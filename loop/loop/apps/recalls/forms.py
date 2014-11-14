from django import forms

from .models import CarMake


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

PRODUCT_CATEGORY_CHOICES = [
    ('Highchairs', 'highchairs'),
    ('Higherchairs', 'higherchairs')
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
    product_category = forms.ChoiceField(choices=PRODUCT_CATEGORY_CHOICES, required=False)

    # motor vehicle
    vehicle_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    vehicle_model = forms.ChoiceField(choices=MODEL_CHOICES, required=False)
    vehicle_make = forms.ModelChoiceField(queryset=CarMake.objects.all(), required=False)
