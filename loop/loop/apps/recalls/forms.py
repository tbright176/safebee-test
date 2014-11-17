from django import forms

from .models import CarMake, ProductCategory


# XXX STUBS
YEAR_CHOICES = [
    ('1999', '1999')
]

MODEL_CHOICES = [
    ('Corolla', 'corolla')
]

MANUFACTURER_CHOICES = [
    ('Tyco', 'tyco'),
    ('Conair', 'conair'),
]


class RecallSignupForm(forms.Form):
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
    manufacturer = forms.ChoiceField(choices=MANUFACTURER_CHOICES, required=False)
    product_category = forms.ModelChoiceField(queryset=ProductCategory.objects.all())

    # motor vehicle
    vehicle_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    vehicle_model = forms.ChoiceField(choices=MODEL_CHOICES, required=False)
    vehicle_make = forms.ModelChoiceField(queryset=CarMake.objects.all(), required=False)


    def clean(self):
        cleaned_data = super(RecallSignupForm, self).clean()

        cat_checkboxes = ['products', 'vehicles', 'foodndrug']

        if not cleaned_data.get('email_alerts') and not cleaned_data.get('phone_alerts'):
            raise forms.ValidationError(
                'You must select to recieve alerts via Email or SMS'
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

            raise forms.ValidationError(
                'You must select either Consumer Products, Motor Vehicles, or Food & Drug'
            )
