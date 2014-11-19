import datetime
import string

from django import forms
from django.conf import settings
from django.utils.text import slugify

from .models import CarMake, ProductCategory, ProductManufacturer


YEAR_CHOICES = tuple((str(n), str(n)) for n in range(1970, datetime.datetime.now().year + 2))

MODEL_CHOICES = [
    ('Corolla', 'corolla')
]

translation_table = string.maketrans('','')
no_digits = translation_table.translate(translation_table, string.digits)

class RecallSignUpForm(forms.Form):
    # delivery options
    email_alerts = forms.BooleanField(required=False)
    phone_alerts = forms.BooleanField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)

    # checkboxes
    products = forms.BooleanField(required=False)
    vehicles = forms.BooleanField(required=False)
    foodndrug = forms.BooleanField(required=False)

    # products
    manufacturer = forms.ModelChoiceField(queryset=ProductManufacturer.objects.all(),
                                          widget=forms.Select(attrs={'class': 'select2 select'}),
                                          empty_label='(Manufacturer)', required=False)
    product_category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(),
                                              widget=forms.Select(attrs={'class': 'select2 select'}),
                                              empty_label='(Category)', required=False)

    # motor vehicle
    vehicle_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False,
                                      widget=forms.Select(attrs={'class': 'select2 select'}))
    vehicle_model = forms.ChoiceField(choices=MODEL_CHOICES, required=False,
                                      widget=forms.Select(attrs={'class': 'select2 select'}))
    vehicle_make = forms.ModelChoiceField(queryset=CarMake.objects.all(), required=False,
                                          widget=forms.Select(attrs={'class': 'select2'}))

    def clean(self):
        cleaned_data = super(RecallSignUpForm, self).clean()

        cat_checkboxes = ['products', 'vehicles', 'foodndrug']

        if not cleaned_data.get('email_alerts') and not cleaned_data.get('phone_alerts'):
            raise forms.ValidationError(
                'You must select to receive alerts via Email or SMS'
            )

        if not cleaned_data.get('email') and not cleaned_data.get('phone_number'):
            if cleaned_data.get('email_alerts'):
                raise forms.ValidationError(
                    'Please enter a valid Email address.'
                )
            else:
                raise forms.ValidationError(
                    'Please enter a valid Phone Number.'
                )

        for checkbox in cat_checkboxes:
            if cleaned_data.get(checkbox, False):
                break
        else:
            raise forms.ValidationError(
                'You must select either Consumer Products, Motor Vehicles, or Food & Drug'
            )

    def clean_phone_number(self):
        phone_num = str(self.cleaned_data['phone_number'])
        just_numbers = phone_num.translate(translation_table, no_digits)

        if (len(just_numbers) < 10) or (len(just_numbers) > 11):
            raise forms.ValidationError(
                'Please enter a valid phone number (XXX-XXX-XXXX or 1-XXX-XXX-XXXX)'
            )

        phone_number = '1-{}{}{}-{}{}{}-{}{}{}{}'.format(*just_numbers[-10:]) # don't judge me

        return phone_number


    def get_topic(self):
        """
        Figure out the topic string that we'll use to either find or create
        the RecallSNSTopic obj, which stores the 'arn' string for each topic.

        Topic Format: SB-<env>-[vehicle|product|foodanddrug]-<topic>
        where <topic> is required for 'vehicle' and 'product', and <env> is one
        of 'Test' or 'Prod'.
        """

        data = self.cleaned_data
        topic = ''
        topic_prefix = 'SB-{}'.format(settings.PROJECT_ENV)
        display_name = ''

        if data['foodndrug']:
            topic_suffix = 'foodanddrug'
            display_name = 'SafeBee - Food and Drug Recalls'

        elif data['products']:
            topic_suffix = ''

            topic_parts = []

            if data['product_category']:
                topic_parts.append(data['product_category'].name)

            if data['manufacturer']:
                topic_parts.append(data['manufacturer'].name)

            subtopic = '-'.join(topic_parts)

            topic_suffix = 'product-{}'.format(subtopic)
            display_name = 'SafeBee - {} Recalls'.format(subtopic)

        elif data['vehicles']:
            vehicle_data = (
                data['vehicle_make'],
                data['vehicle_model'],
                data['vehicle_year']
            )

            topic_suffix = 'vehicle-{}-{}-{}'.format(*vehicle_data)
            display_name = 'SafeBee - {} {} {} Recalls'.format(*vehicle_data)

        topic = '{}-{}'.format(
            topic_prefix,
            topic_suffix
        )

        return slugify(unicode(topic)), display_name
