from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from suit_redactor.widgets import RedactorWidget

from .models import Content, Slide, LoopUser
from .utils import strip_punctuation


EDITOR_OPTIONS = {
    'minHeight': '300',
    'toolbarFixed': True,
    'toolbarFixedBox': True,
    'pastePlainText': False,
    'convertDivs': False,
    'convertLinks': False,
    'convertVideoLinks': False,
    'deniedTags': ['html', 'head', 'link',
                   'body', 'meta',
                   'style', 'applet', 'font', 'span'],
    'plugins': ['asset_manager', 'fullscreen'],
    'buttons': ['html', '|', 'formatting', '|',
                'bold', 'italic', 'deleted', '|',
                'unorderedlist', 'orderedlist',
                'outdent', 'indent', '|',
                'video', 'file', 'table', 'link',
                '|', 'fontcolor', 'backcolor',
                '|', 'alignment', '|',
                'horizontalrule']
}

EDITOR_OPTIONS_NO_PLUGINS = EDITOR_OPTIONS.copy()
EDITOR_OPTIONS_NO_PLUGINS['plugins'] = []


class StagingReferenceMixin(object):

    def check_for_staging_references(self, text):
        if hasattr(settings, 'STAGING_SITE_HOSTNAME'):
            if text:
                if text.find(settings.STAGING_SITE_HOSTNAME) >= 0:
                    error_msg = "This copy contains a reference to the staging site, \"%s\". Please remove and save again." % settings.STAGING_SITE_HOSTNAME
                    raise ValidationError(error_msg)


class ContentAdminForm(forms.ModelForm, StagingReferenceMixin):

    def clean_news_keywords(self):
        """
        Ensure that the number of keywords provided is less than or
        equal to 10. Also removes trailing comma if one exists and strips
        whitespace from each keyword. Commas are the only punctuation
        allowed by Google, so any other characters will be stripped.
        """
        keywords = self.cleaned_data["news_keywords"].strip()
        if keywords:
            if keywords[-1] == ',':
                keywords = keywords[:-1]
            tokens = keywords.split(',')
            if len(tokens) > 10:
                raise ValidationError('No more than 10 keywords are allowed.')
            stripped_tokens = []
            for token in tokens:
                stripped = strip_punctuation(token.strip())
                if stripped:
                    stripped_tokens.append(stripped)
            keywords = ','.join(stripped_tokens)
        return keywords

    def clean(self):
        """
        Ensure that the primary image is supplied before the status is set to
        'Published'.
        """
        cleaned_data = super(ContentAdminForm, self).clean()
        if cleaned_data.get('status', 'D') == 'P' and cleaned_data.get('primary_image') is None:
            raise ValidationError('You must supply a Primary Image when status is "Published"')

        return cleaned_data

    class Meta:
        model = Content
        fields = '__all__'


class ArticleAdminForm(ContentAdminForm):
    body = forms.CharField(widget=\
                           RedactorWidget(editor_options=EDITOR_OPTIONS))

    def clean_body(self):
        """
        Ensure that the body copy does not contain staging links.
        """
        body = self.cleaned_data["body"]
        self.check_for_staging_references(body)
        return body


class PhotoOfTheDayAdminForm(ContentAdminForm):
    caption = forms.CharField(widget=\
                              RedactorWidget(editor_options=\
                                             EDITOR_OPTIONS_NO_PLUGINS),
                              required=False)

    def clean_caption(self):
        """
        Ensure that the caption does not contain staging links
        """
        caption = self.cleaned_data["caption"]
        self.check_for_staging_references(caption)
        return caption


class SlideAdminForm(forms.ModelForm, StagingReferenceMixin):

    def clean_caption(self):
        """
        Ensure that the caption does not contain staging links
        """
        caption = self.cleaned_data["caption"]
        self.check_for_staging_references(caption)
        return caption

    class Meta:
        model = Slide


class LoopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = LoopUser


class LoopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = LoopUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            LoopUser.objects.get(username=username)
        except LoopUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
