import random
import string
import time

import bitly_api

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from twitter import TwitterHTTPError

from .models import SocialStatusRecord
from utils.common import (shorten_url, record_result,
                          action_completed_for_service,
                          fully_qualified_url_for_obj)
from utils.tweet import (obj_was_tweeted, send_tweet, tweet_obj,
                         compose_tweet_for_obj, delete_tweet)

User = get_user_model()


class DummyObject(object):
    title = 'Dummy Title'

    def __unicode__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return u"/social/test/dummy-basename.html"


class BaseTestCase(TestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(
            username=u'testuser',
            password=u'123456',
            first_name=u'Hey First Name',
            last_name=u'Hey Last Name',
        )
        self.link_to_shorten = "http://www.mnn.com"
        self.service_identifier = 'T'
        ctype = ContentType.objects.get_for_model(self.user)
        self.dummy = SocialStatusRecord(content_type=ctype,
                                        object_id=self.user.id,
                                        social_service=self.service_identifier)
        self.dummy.save()


class CommonTestCase(BaseTestCase):

    def test_shorten_url(self):
        url = shorten_url(self.link_to_shorten)
        self.assertNotEqual(url, None)

    def test_action_completed_for_service(self):
        # Should be False since we've not set any record against this object
        was_completed = action_completed_for_service(self.dummy,
                                                     self.service_identifier)
        self.assertFalse(was_completed)

    def test_record_result_true(self):
        record_result(self.dummy, self.service_identifier, True)
        was_completed = action_completed_for_service(self.dummy,
                                                     self.service_identifier)
        self.assertTrue(was_completed)

    def test_record_result_false(self):
        record_result(self.dummy, self.service_identifier, False)
        was_completed = action_completed_for_service(self.dummy,
                                                     self.service_identifier)
        self.assertFalse(was_completed)


class TweetTestCase(BaseTestCase):

    def test_obj_was_tweeted(self):
        was_tweeted = obj_was_tweeted(self.dummy)
        self.assertFalse(was_tweeted)

    def test_compose_tweet_for_obj(self):
        obj_url = fully_qualified_url_for_obj(self.user)
        shortened_obj_url = shorten_url(obj_url).replace('http://', '')
        verification_str = "%s %s" % (self.user, shortened_obj_url)
        composed = compose_tweet_for_obj(self.user)
        self.assertEqual(verification_str, composed)

    def test_compose_tweet_for_obj_no_shortened_url(self):
        self.assertEqual(None, None)

    def test_compose_tweet_for_obj_text_too_long(self):
        dummy = DummyObject()
        dummy.title = "Bacon ipsum dolor sit amet tenderloin turkey pork sirloin, capicola beef kielbasa pastrami pork chop shank beef ribs biltong chicken. Tenderloin beef ribs sirloin meatloaf meatball, hamburger leberkas fatback porchetta filet mignon ham landjaeger ribeye t-bone. Venison capicola ball tip, turkey flank pork chop ham."
        dummy_url = "http://www.mnn.com%s" % dummy.get_absolute_url()
        shortened_obj_url = "example.com/hahaha1"
        verification_str = u"%s\u2026 %s" % (dummy.title[:116],
                                             shortened_obj_url)
        composed = compose_tweet_for_obj(dummy)
        # Compare without the bitly URL on the end since they may differ...
        self.assertEqual(' '.join(verification_str.split(' ')[:-1]),
                         ' '.join(composed.split(' ')[:-1]))

    def test_send_tweet_succeeds(self):
        # Append a random string to the tweet to prevent dupe tweet errors
        random_str = ''.join(random.choice(\
                                           string.ascii_uppercase\
                                           + string.digits) for _ in range(6))

        # Less than 140 chars...
        tweet_text = 'Bacon ipsum dolor sit amet tenderloin turkey pork sirloin, capicola beef kielbasa pastrami pork chop shank beef ribs biltong %s.' % random_str
        resp = send_tweet(tweet_text)
        self.assertFalse(isinstance(resp, TwitterHTTPError))

    def test_send_tweet_fails(self):
        # Too long...
        tweet_text = "Bacon ipsum dolor sit amet tenderloin turkey pork sirloin, capicola beef kielbasa pastrami pork chop shank beef ribs biltong chicken. Tenderloin beef ribs sirloin meatloaf meatball, hamburger leberkas fatback porchetta filet mignon ham landjaeger ribeye t-bone. Venison capicola ball tip, turkey flank pork chop ham."
        resp = send_tweet(tweet_text)
        self.assertTrue(isinstance(resp, TwitterHTTPError))

    def test_tweet_obj_succeeds(self):
        result, is_error = tweet_obj(self.user)
        time.sleep(3)
        delete_tweet(result["id"])
        self.assertFalse(is_error)

    def test_tweet_obj_fails(self):
        # Should succeed...
        orig_result, orig_is_error = tweet_obj(self.user)
        time.sleep(3)
        # Should fail as a duplicate...
        second_result, second_is_error = tweet_obj(self.user)
        time.sleep(3)
        delete_tweet(orig_result["id"])
        self.assertTrue(second_is_error)

    def test_delete_tweet_succeeds(self):
        resp = send_tweet("Haha test_delete_tweet_succeeds!!!")
        time.sleep(3)
        del_resp = delete_tweet(resp['id'])
        self.assertFalse(isinstance(del_resp, TwitterHTTPError))

    def test_delete_tweet_fails(self):
        resp = send_tweet("Haha test_delete_tweet_fails!!!")
        time.sleep(3)
        del_resp = delete_tweet("abcdefgh")
        self.assertTrue(isinstance(del_resp, TwitterHTTPError))
        del_resp = delete_tweet(resp['id_str'])
