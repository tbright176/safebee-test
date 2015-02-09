from django import forms

from .models import Question, PlayerResponse

class QuestionInlineFormSet(forms.models.BaseInlineFormSet):

    def clean(self):
        test = super(QuestionInlineFormSet, self).clean()

        for question in self.forms:
            if question.cleaned_data.has_key('id'):
                break
        else:
            raise forms.ValidationError('There must be atleast one valid Question.')


class AnswerInlineFormSet(forms.models.BaseInlineFormSet):

    def clean(self):
        super(AnswerInlineFormSet, self).clean()

        for answer in [form for form in self.forms if form.cleaned_data.has_key('id')]:
            deleted = answer.cleaned_data.get('DELETE', False)
            correct = answer.cleaned_data.get('correct', False)
            if not deleted and correct:
                return

        raise forms.ValidationError('You must have atleast one correct answer per question.')


class QuestionForm(forms.models.ModelForm):
    class Meta:
        model = Question


class ResponseForm(forms.models.ModelForm):
    class Meta:
        model = PlayerResponse
