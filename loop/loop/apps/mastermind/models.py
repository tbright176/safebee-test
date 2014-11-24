# TODO:
# 1. randomize answers

from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.db import models

from asset_manager.models import Image
from core.models import Content, StreamItem


class Quiz(Content):

    results_image = models.ForeignKey(Image, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('mastermind:quiz',
                       kwargs={'basename': self.basename,
                               'category': self.category.slug})

    def get_results_image(self):
        if self.results_image:
            return self.results_image
        else:
            return self.primary_image


class Question(models.Model):

    text = models.CharField(max_length=200)
    background_image = models.ForeignKey(Image, related_name='+', null=True, blank=True)
    explanation = models.TextField()

    def __unicode__(self):
        return self.text

    def get_image(self):
        if self.background_image:
            return self.background_image
        else:
            return self.quizquestion.quiz.primary_image


class QuizQuestion(models.Model):

    order = models.PositiveIntegerField()
    quiz = models.ForeignKey('Quiz', related_name='questions')
    question = models.OneToOneField('Question')

    class Meta:
        ordering = ['order',]

    def __unicode__(self):
        return self.question.text


class Answer(models.Model):

    question = models.ForeignKey('Question')
    correct = models.BooleanField(default=False)
    choice = models.CharField(max_length=100)

    def __unicode__(self):
        return self.choice


class ScoreRange(models.Model):

    quiz = models.ForeignKey('Quiz')
    lower_limit = models.PositiveSmallIntegerField()
    upper_limit = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=120)


class PlayerAnswerSet(models.Model):

    session = models.ForeignKey(Session)
    quiz = models.ForeignKey('Quiz', related_name='+')

    def score(self):
        """
        Returns a tuple Score, ScoreRange
        """
        num_correct = sum([response.response.correct for response in self.playerresponse_set.all()])
        try:
            score_range = self.quiz.scorerange_set.get(lower_limit__lte=num_correct, upper_limit__gte=num_correct)
        except ScoreRange.DoesNotExist:
            score_range = None
        return num_correct, score_range

class PlayerResponse(models.Model):

    parent = models.ForeignKey('PlayerAnswerSet')
    question = models.ForeignKey('Question', related_name='+')
    response = models.ForeignKey('Answer', related_name='+')
