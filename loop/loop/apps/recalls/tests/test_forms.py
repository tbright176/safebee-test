from django.test import TestCase
from recalls.forms import RecallSignUpForm


class RecallSignUpFormTestCase(TestCase):
    def setUp(self):
        self.data = {
            'phone_alerts': True,
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

        self.assertEqual(form.cleaned_data['phone_number'], '1-123-123-1234')
        self.assertEqual(form2.cleaned_data['phone_number'], '1-123-123-1234')
