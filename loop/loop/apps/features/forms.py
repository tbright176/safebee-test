from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from suit_redactor.widgets import RedactorWidget

from core.admin_forms import ContentAdminForm, EDITOR_OPTIONS_NO_PLUGINS


class FeatureAdminForm(ContentAdminForm):
    intro_copy = forms.CharField(widget=\
                                 RedactorWidget(editor_options=EDITOR_OPTIONS_NO_PLUGINS))

    def clean_intro_copy(self):
        """
        Ensure that the intro copy does not contain staging links.
        """
        intro_copy = self.cleaned_data["intro_copy"]
        self.check_for_staging_references(intro_copy)
        return intro_copy
