import datetime
import string

from django import forms
from django.conf import settings
from django.utils.text import slugify

from .models import CarMake, CarModel, ProductCategory, ProductManufacturer


translation_table = string.maketrans('','')
no_digits = translation_table.translate(translation_table, string.digits)


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class RecallSignUpForm(forms.Form):
    # delivery options
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)

    # checkboxes
    products = forms.BooleanField(required=False)
    vehicles = forms.BooleanField(required=False)
    foodndrug = forms.BooleanField(required=False)

    # products
    manufacturer = forms.ModelChoiceField(queryset=ProductManufacturer.objects.all(),
                                          widget=forms.Select(attrs={
                                              'class': 'select2',
                                              'data-placeholder': 'Select a Manufacturer'
                                          }),
                                          empty_label='', required=False)
    product_category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(),
                                              widget=forms.Select(attrs={
                                                  'class': 'select2',
                                                  'data-placeholder': 'Select a Category'
                                              }),
                                              empty_label='', required=False)

    # motor vehicle
    vehicle_year = ChoiceFieldNoValidation(choices=tuple([('','')]), required=False,
                                           widget=forms.Select(attrs={
                                               'class': 'select2',
                                               'data-placeholder': 'Select a Vehicle Year'
                                           }))
    vehicle_model = ChoiceFieldNoValidation(choices=tuple([('','')]), required=False,
                                            widget=forms.Select(attrs={
                                                'class': 'select2',
                                                'data-placeholder': 'Select a Vehicle Model'
                                            }))
    vehicle_make = forms.ModelChoiceField(queryset=CarMake.objects.all(), required=False,
                                          empty_label='',
                                          widget=forms.Select(attrs={
                                              'class': 'select2',
                                              'data-placeholder': 'Select a Vehicle Make'
                                          }))

    def clean(self):
        cleaned_data = super(RecallSignUpForm, self).clean()

        cat_checkboxes = ['products', 'vehicles', 'foodndrug']

        if not cleaned_data.get('email') and not cleaned_data.get('phone_number'):
            raise forms.ValidationError(
                'You must enter a valid Email or Phone Number'
            )

        for checkbox in cat_checkboxes:
            if cleaned_data.get(checkbox, False):
                break
        else:
            raise forms.ValidationError(
                'You must select either Consumer Products, Motor Vehicles, or Food & Drug'
            )

        if cleaned_data.get('phone_number'):
            phone_num = str(self.cleaned_data['phone_number'])
            just_numbers = phone_num.translate(translation_table, no_digits)

            if (len(just_numbers) < 10) or (len(just_numbers) > 11):
                raise forms.ValidationError(
                    'Please enter a valid phone number (XXX-XXX-XXXX or 1-XXX-XXX-XXXX)'
                )

            cleaned_data['phone_number'] = '1-{}{}{}-{}{}{}-{}{}{}{}'.format(*just_numbers[-10:]) # don't judge me

        if cleaned_data.get('vehicles'):
            required_vehicle_fields = ['vehicle_make', 'vehicle_model', 'vehicle_year']
            for vehicle_field in ['vehicle_make', 'vehicle_model', 'vehicle_year']:
                if not self.data.has_key(vehicle_field) or self.data[vehicle_field] is None:
                    raise forms.ValidationError(
                        'Make/Model/Year are required for Vehicles'
                    )

                vehicle_value = self.data.get(vehicle_field)

                if vehicle_field == 'vehicle_make':
                    vehicle_value = CarMake.objects.get(pk=vehicle_value)

                if vehicle_field == 'vehicle_model':
                    vehicle_value = CarModel.objects.get(pk=vehicle_value)

                cleaned_data[vehicle_field] = vehicle_value

        return cleaned_data

    def get_topics(self):
        """
        Figure out the topic string that we'll use to either find or create
        the RecallSNSTopic obj, which stores the 'arn' string for each topic.

        Topic Format: SB-<env>-[vehicle|product|foodanddrug]-<topic>
        where <topic> is required for 'vehicle' and 'product', and <env> is one
        of 'Test' or 'Prod'.
        """

        data = self.cleaned_data
        topics = []
        topic_prefix = 'SB-{}'.format(settings.PROJECT_ENV)
        display_name = ''

        def format_topic(suffix):
            return slugify(unicode('{} - {}'.format(topic_prefix, suffix)))

        if data['foodndrug']:
            topics.append({
                'name': format_topic('foodanddrug'),
                'display': 'SafeBee - Food and Drug Recalls'
            })

        if data['products']:
            topic_suffix = ''
            topic_parts = []

            if data['product_category']:
                topic_parts.append(data['product_category'].name)
            if data['manufacturer']:
                topic_parts.append(data['manufacturer'].name)

            subtopic = '-'.join(topic_parts)

            topics.append({
                'name': format_topic('product-{}'.format(subtopic)),
                'display': 'SafeBee - {} Recalls'.format(subtopic)
            })

        if data['vehicles']:
            vehicle_data = (
                data['vehicle_make'].name,
                data['vehicle_model'].name,
                self.data['vehicle_year']
            )

            topics.append({
                'name': format_topic('vehicle-{}-{}-{}'.format(*vehicle_data)),
                'display':'SafeBee - {} {} {} Recalls'.format(*vehicle_data)
            })

        return topics
