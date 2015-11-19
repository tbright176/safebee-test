from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

from sitemaps import (ArticleSitemap, AuthorSitemap, SlideshowSitemap,
                      FlatPageSitemap, CategorySitemap, TagSitemap, QuizSitemap)

sitemaps = {
    'articles': ArticleSitemap,
    'slideshows': SlideshowSitemap,
    'pages': FlatPageSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
    'quizzes': QuizSitemap,
}

urlpatterns = patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}, name='sitemap-index'),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^admin/settings/', include('dbsettings.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newsletter/$', TemplateView.as_view(template_name='misc/newsletter.html'), name="newsletter_signup"),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt'), name="robots_txt"),
    url(r'^404/$', TemplateView.as_view(template_name='404.html'), name="404_page"),
    url(r'^quizzes/', include('mastermind.urls', namespace='mastermind')),
    url(r'^buzz/$', include('buzz.urls', namespace='buzz')),
    url(r'^features/', include('features.urls')),
    url(r'^recalls/', include('recalls.urls')),
    url(r'^', include('core.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'404\.html$', TemplateView.as_view(template_name="404.html"),
            name="test_404"),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
