from django.conf.urls import patterns, url

from .feeds import (LatestContentFeed, AuthorFeed, CategoryFeed,
                    MostPopularFeed, MostPopularRecallsFeed, TagFeed)
from .views import (AuthorStreamIndex, BlogView, CategoryStreamIndex,
                    StreamIndex, TagStreamIndex, ArticleView, InfographicView,
                    PhotoBlogView, PhotoOfTheDayView, SlideShowView,
                    TipsListView, RSSLandingPageView)


urlpatterns = patterns('',
    # Home page
    url(r'^$', 'hubpage.views.home_page', name='core_home_page'),
    url(r'^rss/$', RSSLandingPageView.as_view(), name='core_rss_landing'),
    url(r'^(?:page/(?P<page_num>\d+)/)?$', StreamIndex.as_view(), name='core_home'),

    # Feed URLs
    url(r'^feeds/latest/$', LatestContentFeed(),
        name="core_latest_content_feed"),
    url(r'^feeds/most-popular/$', MostPopularFeed(),
        name="core_most_popular_feed"),
    url(r'^feeds/most-popular-recalls/$', MostPopularRecallsFeed(),
        name="core_most_popular_recalls_feed"),
    url(r'^feeds/category/(?P<slug>[-,\+\w]+)/$',
        CategoryFeed(), name="core_category_feed"),
    url(r'^feeds/tag/(?P<slug>[-,\+\w]+)/$',
        TagFeed(), name="core_tag_feed"),
    url(r'^feeds/author/(?P<basename>[-\w]+)/$',
        AuthorFeed(), name="core_author_feed"),

    # Infographics with category and optional sub-category
    url(r'^infographics/(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)$',
        InfographicView.as_view(), name='core_infographic'),

    # Photo Blogs with category and optional sub-category
    url(r'^photoblogs/(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)$',
        PhotoBlogView.as_view(), name='core_photoblog'),

    # Tips Lists with category and optional sub-category
    url(r'^lists/(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)$',
        TipsListView.as_view(), name='core_tipslist'),

    # Blogs with category and optional sub-category
    url(r'^blogs/(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)$',
        BlogView.as_view(), name='core_blog'),

    # Articles with category and optional sub-category
    url(r'^(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)$',
        ArticleView.as_view(), name='core_article'),

    # Photos with category and optional sub-category
    url(r'^photos/(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)?(?:/page/(?P<page_num>\d+))?/$',
        PhotoOfTheDayView.as_view(), name='core_photooftheday'),

    # Slideshow with category and optional sub-category
    url(r'^slideshows/(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)?(?:/page/(?P<page_num>\d+))?/$',
        SlideShowView.as_view(), name='core_slideshow'),

    # Tag index page for a category that is optionally a sub-category
    url(r'^authors/(?P<author_slug>[-,\+\w]+)(?:/page/(?P<page_num>\d+))?/$',
        AuthorStreamIndex.as_view(), name='core_author_index'),

    # Tag index page for a category that is optionally a sub-category
    url(r'^tag/(?P<tag_slug>[-,\+\w]+)(?:/page/(?P<page_num>\d+))?/$',
        TagStreamIndex.as_view(), name='core_tag_index'),

    # Category index page for a category that is optionally a sub-category
    url(r'^(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?(?:/page/(?P<page_num>\d+))?/$',
        CategoryStreamIndex.as_view(), name='core_category_index'),
)
