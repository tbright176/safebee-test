from django.contrib.auth import get_user_model
from django.test import TestCase

from core.admin_forms import ContentAdminForm
from core.models import Article, Category

User = get_user_model()


class ContentAdminFormTests(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category = Category.objects.create(name="Boo", slug="boo")
        self.content = Article.objects.create(author=self.author,
                                              title="Title",
                                              basename="basename-hey",
                                              category=self.category,
                                              description="Heyyyyyyy")

        self.content_data = {'author': self.author.id,
                             'title': self.content.title,
                             'basename': self.content.basename,
                             'category': self.category.id,
                             'description': self.content.description,
                             'status': self.content.status,
                             'publication_date': self.content.publication_date}

    def test_good_news_keywords_validation(self):
        ok_keywords = 'hey1, hey2, hey3'
        result = 'hey1,hey2,hey3'
        self.content_data['news_keywords'] = ok_keywords
        ca_form = ContentAdminForm(self.content_data, instance=self.content)
        self.assertTrue(ca_form.is_valid())
        self.assertEqual(ca_form.cleaned_data['news_keywords'], result)

    def test_good_news_keywords_end_in_comma_validation(self):
        ok_keywords = 'hey1, hey2, hey3,'
        result = 'hey1,hey2,hey3'
        self.content_data['news_keywords'] = ok_keywords
        ca_form = ContentAdminForm(self.content_data, instance=self.content)
        self.assertTrue(ca_form.is_valid())
        self.assertEqual(ca_form.cleaned_data['news_keywords'], result)

    def test_too_many_news_keywords_validation(self):
        bad_keywords = 'a,b,c,d,e,f,g,h,i,j,k,l'
        self.content_data['news_keywords'] = bad_keywords
        ca_form = ContentAdminForm(self.content_data, instance=self.content)
        self.assertFalse(ca_form.is_valid())

    def test_good_news_keywords_has_non_comma_punctuation(self):
        ok_keywords = u".hey1.#, h@*ey2, hey(%3!,!"
        result = 'hey1,hey2,hey3'
        self.content_data['news_keywords'] = ok_keywords
        ca_form = ContentAdminForm(self.content_data, instance=self.content)
        self.assertTrue(ca_form.is_valid())
        self.assertEqual(ca_form.cleaned_data['news_keywords'], result)
