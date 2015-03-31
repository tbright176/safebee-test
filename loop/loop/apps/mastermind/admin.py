import copy
import re

from suit.admin import (SortableModelAdmin, SortableStackedInline,
                        SortableTabularInline)

from django.contrib import admin
from django.http import HttpResponse

from asset_manager.widgets import ImageAssetWidget
from core.admin import ContentAdmin, RelatedInline

from .forms import QuestionInlineFormSet, AnswerInlineFormSet
from .models import (Quiz, Question, Answer, ScoreRange, QuizQuestion)


class AnswerInline(admin.TabularInline):
    extra = 3
    max_num = 4
    model = Answer
    formset = AnswerInlineFormSet


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [
        AnswerInline,
    ]

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if "_popup" in request.REQUEST:
            return HttpResponse(
                u'<script>window.opener.dismissAddAnotherPopup(window, "{obj_id}", "{obj_name}");</script>'.format(
                    obj_id=obj.pk,
                    obj_name=re.escape(obj.text),
                ))
        else:
            return super(QuestionAdmin, self).response_add(
                request, obj, post_url_continue=post_url_continue)

    def response_change(self, request, obj):
        if "_popup" in request.REQUEST:
            return HttpResponse(
                u'<script>window.opener.dismissAddAnotherPopup(window, "{obj_id}", "{obj_name}");</script>'.format(
                    obj_id=obj.pk,
                    obj_name=re.escape(obj.text),
            ))
        else:
            return super(QuestionAdmin, self).response_change(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'background_image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(QuestionAdmin, self).formfield_for_foreignkey(db_field,
                                                                    request,
                                                                    **kwargs)


class QuestionInline(SortableStackedInline):
    extra = 1
    model = QuizQuestion


class ScoreRangeInline(admin.TabularInline):
    model = ScoreRange


class QuizAdmin(ContentAdmin):
    model = Quiz
    inlines = [
        QuestionInline,
        ScoreRangeInline,
        RelatedInline,
    ]
    change_form_template = 'admin/quiz_change_form.html'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(QuizAdmin, self).get_fieldsets(request, obj)
        fieldsets_copy = copy.deepcopy(fieldsets)
        for fieldset in fieldsets_copy:
            if fieldset[0] == 'Images':
                fieldset[1]['fields'] = ('primary_image', 'social_image', 'promo_image', 'results_image')
        return fieldsets_copy

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'results_image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(QuizAdmin, self).formfield_for_foreignkey(db_field,
                                                                    request,
                                                                    **kwargs)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
