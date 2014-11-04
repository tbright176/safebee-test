from disqusapi import DisqusAPI

from django.conf import settings


class DisqusAPIClient(object):

    def __init__(self):
        self.disqus = DisqusAPI(settings.DISQUS_API_SECRET,
                                settings.DISQUS_API_KEY)

    def get_hot_threads(self):
        return self.disqus.threads\
                          .listHot(forum=settings.DISQUS_FORUM_SHORTNAME)

    def get_popular_threads(self):
        return self.disqus.threads\
                          .listPopular(forum=settings.DISQUS_FORUM_SHORTNAME)


if __name__ == '__main__':
    d = DisqusAPIClient()
    print d.get_popular_threads()
