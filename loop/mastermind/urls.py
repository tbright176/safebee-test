from django.conf.urls import patterns, url

from .views import QuizDetailView, QuestionDetailView, PlayerResponseCreateView, QuizResultsView


urlpatterns = patterns('loop.mastermind.views',
    url(r'^(?P<category>[-,\+\w]+)/(?P<basename>[-,\+\w]+)/$', QuizDetailView.as_view(), name='quiz'),
)
