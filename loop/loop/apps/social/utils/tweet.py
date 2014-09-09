import unicodedata
from urlparse import urlparse

import bitly_api
from twitter import OAuth, Twitter, TwitterHTTPError

from django.conf import settings

from .common import (shorten_url, action_completed_for_service,
                     record_result, fully_qualified_url_for_obj)


def twitter_connection():
    return Twitter(auth=OAuth(settings.TWITTER_OAUTH_ACCESS_TOKEN,
                              settings.TWITTER_OAUTH_SECRET_TOKEN,
                              settings.TWITTER_API_KEY,
                              settings.TWITTER_API_SECRET_KEY))


def send_tweet(text):
    twit = twitter_connection()
    try:
        resp = twit.statuses.update(status=text)
        return resp
    except TwitterHTTPError, e:
        return e


def delete_tweet(tweet_id):
    twit = twitter_connection()
    try:
        resp = twit.statuses.destroy(id=tweet_id)
        return resp
    except TwitterHTTPError, e:
        return e


def obj_was_tweeted(obj):
    return action_completed_for_service(obj, 'T')


def tweet_obj(obj):
    is_error = True
    result = None
    tweet_text = compose_tweet_for_obj(obj)
    if tweet_text:
        result = send_tweet(tweet_text)

        if not isinstance(result, TwitterHTTPError):
            is_error = False

    record_result(obj, 'T', (not is_error))
    return result, is_error


def compose_tweet_for_obj(obj):
    text = u"%s" % obj

    # Normalize text to compose Unicode characters that might be
    # represented by a shorter sequence to save space
    normalized = unicodedata.normalize('NFC', text.strip())

    # bitly-ize that thang...
    shortened_url = shorten_url(fully_qualified_url_for_obj(obj))
    if not shortened_url:
        # Some error occurred, return None...
        return

    # Strip scheme since it's not required for tweet
    parsed = urlparse(shortened_url)
    shortened_url = parsed.netloc + parsed.path

    # Length of shortened URL plus 1 for a space between title and URL
    shortened_length = len(shortened_url) + 1
    text_length = len(normalized) + shortened_length

    # Truncate text if too long...
    if text_length > 140:
        # Reduce the text by the overage
        normalized = normalized[:((text_length - 138) * -1)]

        # Truncate at the last complete word...
        normalized = ' '.join(normalized.split(' ')[:-1])

        # Add unicode ellipsis to save space
        normalized += u"\u2026"

    text = u"%s %s" % (normalized, shortened_url)
    return text
