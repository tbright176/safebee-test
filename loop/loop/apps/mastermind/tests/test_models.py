import datetime
import pytz

from django.contrib.sessions.models import Session
from django.test import TestCase


from mastermind.models import Quiz, Question, Answer, PlayerResponse, PlayerAnswerSet


class TestPlayerAnswerSetModelTestCase(TestCase):

    fixtures = ['initial_groups', 'test_super_user', 'test_quiz']

    def setUp(self):

        user_session = Session.objects.create(
            session_key='123',
            session_data='',
            expire_date=datetime.datetime(2201, 5, 10, 12, 0, 0)
        )

        self.answer_set = PlayerAnswerSet.objects.create(
            session=user_session,
            quiz=Quiz.objects.all()[0]
        )

    def test_next_question(self):
        # no responses, so should return first question
        question = self.answer_set.next_question()

        self.assertEqual(question.order, 1)

        # grab an arbitrary answer choice
        answer = Answer.objects.filter(question=question)[0]

        response = PlayerResponse.objects.create(
            parent=self.answer_set,
            question=question,
            response=answer,
        )

        question = self.answer_set.next_question()
        self.assertEqual(question.order, 2)
