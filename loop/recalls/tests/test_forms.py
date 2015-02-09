from django.test import TestCase
from recalls.forms import RecallSignUpForm

from .factories import CarMakeFactory, CarModelFactory


class RecallSignUpFormTestCase(TestCase):
    def setUp(self):
        self.car_make = CarMakeFactory()
        self.car_model = CarModelFactory(make=self.car_make)
        self.data = {
            'phone_number': '1231231234',
            'foodndrug': True
        }

    def test_clean_phone(self):
        form = RecallSignUpForm(data=self.data)
        form.is_valid()

        data2 = self.data.copy()
        data2['phone_number'] = '123-123-1234'
        form2 = RecallSignUpForm(data=data2)
        form2.is_valid()

        bad_data = self.data.copy()
        bad_data['phone_number'] = '123'
        bad_form = RecallSignUpForm(data=bad_data)

        self.assertEqual(form.cleaned_data['phone_number'], '1-123-123-1234')
        self.assertEqual(form2.cleaned_data['phone_number'], '1-123-123-1234')
        self.assertFalse(bad_form.is_valid())

    def test_vehicle_validation(self):

        data = {
            'email': 'test@email.com',
            'vehicles': True,
            'vehicle_make': self.car_make.pk,
        }

        form = RecallSignUpForm(data=data)

        self.assertFalse(form.is_valid())

    def test_vehicle(self):
        data = {
            'email': 'test@email.com',
            'vehicles': True,
            'vehicle_make': self.car_make.pk,
            'vehicle_model': self.car_model.pk,
            'vehicle_year': '1999'
        }

        form = RecallSignUpForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['vehicle_make'], self.car_make)
        self.assertEqual(form.cleaned_data['vehicle_model'], self.car_model)
        self.assertEqual(form.cleaned_data['vehicle_year'], '1999')
