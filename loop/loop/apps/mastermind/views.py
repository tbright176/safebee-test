from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView

from .models import Quiz, Question, PlayerAnswerSet, Answer, PlayerResponse
from .forms import ResponseForm

def get_player_session(request, quiz):
    """
    extracts the session and player responses for the current user.

    returns Session, PlayerAnswerSet

    """

    user_session = Session.objects.get(session_key=request.session.session_key)
    player_answers, _ = PlayerAnswerSet.objects.get_or_create(
        session=user_session,
        quiz=quiz
    )
    return player_answers


class QuizDetailView(DetailView):
    """

    Detail view for Quiz.

    This will serve as the landing page for the quiz, which will handle the initial load.
    The template contains javascript that will load questions via AJAX.

    """

    queryset = Quiz.objects.all()
    context_object_name = 'content_item'
    slug_field = 'basename'
    slug_url_kwarg = 'basename'

    def get_context_data(self, **kwargs):
        context = {}
        context['questions'] = [qq.question for qq in self.object.questions.select_related('question').order_by('order')]
        context.update(kwargs)
        return super(QuizDetailView, self).get_context_data(**context)


class QuestionDetailView(DetailView):
    """
    Question detail view.  Will return json for the quiz question requested.

    """
    queryset = Question.objects.all()
    template_name = 'mastermind/question_detail.html'
    context_object_name = 'question'
    slug_field = 'basename'
    slug_url_kwarg = 'basename'


class PlayerResponseCreateView(CreateView):
    form_class = ResponseForm
    model = PlayerResponse

    def post(self, request, *args, **kwargs):

        answer_id = self.request.POST.get('answer')
        button = self.request.POST.get('quiz-btn')
        next_question = None
        quiz = Quiz.objects.get(basename=self.kwargs['basename'])

        if answer_id:
            answer = Answer.objects.get(pk=answer_id)
            player_answers = get_player_session(self.request, quiz)

            player_response, created = PlayerResponse.objects.get_or_create(
                parent=player_answers,
                question=answer.question,
                defaults={'response': answer}
            )
            if not created:
                player_response.response = answer
                player_response.save()

            next_question = answer.question.next_question()
        elif button:
            if button == 'start-quiz':
                next_question = quiz.question_set.order_by('order')[0]

        if next_question:
            return redirect(reverse('mastermind:question', kwargs={'pk': next_question.pk}))
        return redirect(reverse('mastermind:results', kwargs={'basename': quiz.basename}))


class QuizResultsView(QuizDetailView):
    template_name = 'mastermind/player_results.html'

    def get_context_data(self, **kwargs):
        answers = get_player_session(self.request, self.object)
        num_correct, score_range = answers.score()
        context = {}
        context['num_correct'] = num_correct
        context['score_range'] = score_range
        context.update(kwargs)
        return super(QuizResultsView, self).get_context_data(**context)
