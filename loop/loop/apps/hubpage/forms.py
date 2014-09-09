from django import forms
from django.core.exceptions import ValidationError

from .models import ContentModule, HubPage


class HubPageAdminForm(forms.ModelForm):

    def clean_set_as_homepage(self):
        is_homepage = self.cleaned_data['set_as_homepage']
        if not is_homepage:
            other_homepages = HubPage.objects.filter(set_as_homepage=True)\
                              .exclude(id=self.instance.id)
            if not other_homepages:
                raise ValidationError('There must be at least one home page')

        return is_homepage

    class Meta:
        model = HubPage


class HubPageCategoryContentModuleAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HubPageCategoryContentModuleAdminForm,
              self).__init__(*args, **kwargs)
        self.fields['module'].queryset = ContentModule.objects.filter(category__isnull=False)



class HubPageContentModuleAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HubPageContentModuleAdminForm,
              self).__init__(*args, **kwargs)
        self.fields['module'].queryset = ContentModule.objects.filter(category__isnull=True)
