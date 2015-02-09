import datetime

from pytz import timezone as pytz_timezone
from urlparse import urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from core.models import Article, Category, StreamItem, Tag

User = get_user_model()


class HomePageTestCase(TestCase):

    def setUp(self):
        self.home_page_url = reverse('core_home')

    def test_page_load(self):
        response = self.client.get(self.home_page_url)
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        site = Site.objects.get_current()
        response = self.client.get(self.home_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_site'].name, site.name)

    def test_home_page_page_1_redirect(self):
        url = reverse('core_home', kwargs={'page_num': 1})
        final_url = reverse('core_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(urlparse(response['location']).path,
                         final_url)


class ArticleModelTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category = Category.objects.create(name="Boo", slug="boo")
        self.sub_category = Category.objects.create(name="Radley",
                                                    slug="radley",
                                                    parent=self.category)
        self.article = Article.objects.create(title="Testing StreamItem!",
                                              basename="testing-streamitem",
                                              category=self.category,
                                              author=self.author)


    def test_article_unicode_method(self):
        self.assertEqual(self.article.title, "%s" % self.article)

    def test_article_get_absolute_url_method_no_sub_category(self):
        reversed = reverse('core_article',
                           kwargs={'basename': self.article.basename,
                                   'category_slug': self.category.slug})
        self.assertEqual(reversed, self.article.get_absolute_url())

    def test_article_get_absolute_url_method_with_sub_category(self):
        self.article.category = self.sub_category
        reversed = reverse('core_article',
                           kwargs={'basename': self.article.basename,
                                   'sub_category_slug': self.sub_category.slug,
                                   'category_slug': self.category.slug})
        self.assertEqual(reversed, self.article.get_absolute_url())

    def test_article_author(self):
        self.assertEqual(self.author, self.article.author)

    def test_article_default_canonical_url(self):
        site = Site.objects.get_current()
        reversed = reverse('core_article',
                           kwargs={'basename': self.article.basename,
                                   'category_slug': self.category.slug})
        expected_url = "http://%s%s" % (site.domain, reversed)
        self.assertEqual(expected_url, self.article.get_canonical_url())

    def test_article_canonical_url(self):
        expected_url = "http://www.hahahahaha.com/booo.html"
        self.article.canonical_url = expected_url
        self.assertEqual(expected_url, self.article.get_canonical_url())

    def test_article_get_title(self):
        self.assertEqual(self.article.title, self.article.get_title())

    def test_article_page_title_get_title(self):
        self.article.page_title = "This is a custom page title."
        self.assertNotEqual(self.article.title, self.article.get_title())
        self.assertEqual(self.article.page_title, self.article.get_title())

    def test_past_article_scheduled_publishing(self):
        eastern = pytz_timezone('US/Eastern')
        date_in_past = eastern.localize(datetime.datetime(2010, 5, 10, 12, 0, 0))
        self.article.status = 'S'
        self.article.publication_date = date_in_past
        self.article.save()
        call_command('publish_scheduled_content')
        self.article = Article.objects.get(pk=self.article.pk)
        self.assertEqual('P', self.article.status)

    def test_future_article_scheduled_publishing(self):
        eastern = pytz_timezone('US/Eastern')
        date_in_future = eastern.localize(\
                                          datetime.datetime(2201, 5, 10,
                                                            12, 0, 0))
        self.article.status = 'S'
        self.article.publication_date = date_in_future
        self.article.save()
        call_command('publish_scheduled_content')
        self.article = Article.objects.get(pk=self.article.pk)
        self.assertEqual('S', self.article.status)


class ArticleModelManagersTestCase(TestCase):

    def setUp(self):
        statii = ['D', 'P', 'M', 'S']
        author = User.objects.create_user(username='ben',
                                          email='blah@blah.com',
                                          password='123456')
        category = Category.objects.create(name="Boo", slug="boo")
        for i in range(44):
            Article.objects.create(title="uggghhhh %d" % i,
                                   basename="uggghhhh-%d" % i,
                                   category=category,
                                   status=statii[i % len(statii)],
                                   author=author,
                                   description="Description %d" % i)

    def test_published_content(self):
        items = Article.published.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('P', item.status)

    def test_draft_content(self):
        items = Article.draft.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('D', item.status)

    def test_scheduled_content(self):
        items = Article.scheduled.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('S', item.status)

    def test_needs_moderation_content(self):
        items = Article.needs_moderation.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('M', item.status)


class StreamItemPaginationTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Boo", slug="boo")
        author = User.objects.create_user(username='ben',
                                          email='blah@blah.com',
                                          password='123456')
        for i in range(int(settings.CORE_DEFAULT_INDEX_LENGTH * 2.5)):
            Article.objects.create(title="Pagination Test %d" % i,
                                   basename="pagination-test-%d" % i,
                                   category=self.category,
                                   status='P',
                                   author=author,
                                   description="Description %d" % i)

    def test_nonexistent_page_num(self):
        url = reverse('core_category_index',
                      kwargs={'category_slug': self.category.slug,
                              'page_num': 30})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_page_1_redirect(self):
        url = reverse('core_category_index',
                      kwargs={'category_slug': self.category.slug,
                              'page_num': 1})
        final_url = reverse('core_category_index',
                      kwargs={'category_slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(urlparse(response['location']).path,
                         final_url)

    def test_page_2_response(self):
        url = reverse('core_category_index',
                      kwargs={'category_slug': self.category.slug,
                              'page_num': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['stream_items']),
                         settings.CORE_DEFAULT_INDEX_LENGTH)


class StreamItemManagersTestCase(TestCase):

    def setUp(self):
        statii = ['D', 'P', 'M', 'S']
        author = User.objects.create_user(username='ben',
                                          email='blah@blah.com',
                                          password='123456')
        category = Category.objects.create(name="Boo", slug="boo")
        for i in range(44):
            Article.objects.create(title="uggghhhh %d" % i,
                                   basename="uggghhhh-%d" % i,
                                   category=category,
                                   status=statii[i % len(statii)],
                                   author=author,
                                   description="Description %d" % i)

    def test_published_content(self):
        items = StreamItem.published.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('P', item.status)

    def test_draft_content(self):
        items = StreamItem.draft.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('D', item.status)

    def test_scheduled_content(self):
        items = StreamItem.scheduled.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('S', item.status)

    def test_needs_moderation_content(self):
        items = StreamItem.needs_moderation.all()
        self.assertEqual(items.count(), 11)
        for item in items:
            self.assertEqual('M', item.status)


class StreamItemModelTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category = Category.objects.create(name="Boo", slug="boo")
        self.content_type = ContentType.objects.get(app_label="core",
                                                    model="article")
        self.article = Article.objects.create(title="Testing StreamItem!",
                                              basename="testing-streamitem",
                                              category=self.category,
                                              author=self.author,
                                              status='P')

    def test_content_object_exists(self):
        stream_item = StreamItem.objects.create(category=self.category,
                                                content_type=self.content_type,
                                                object_id=self.article.id,
                                                author=self.author)
        self.assertTrue(hasattr(stream_item, 'content_object'))

    def test_content_type_identifier_method(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual("core_article", stream_item.content_type_identifier())

    def test_stream_item_created_from_article_post_save(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertIsInstance(stream_item, StreamItem)

    def test_stream_item_pub_date_matches_article_pub_date(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual(self.article.publication_date,
                         stream_item.publication_date)

    def test_stream_item_pub_status_matches_article_pub_status(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual(self.article.status, stream_item.status)

    def test_article_pub_date_change_updates_stream_item(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual(self.article.publication_date,
                         stream_item.publication_date)
        self.article.publication_date = timezone.now()
        self.article.save()
        stream_item = StreamItem.objects.get(pk=stream_item.id)
        self.assertEqual(self.article.publication_date,
                         stream_item.publication_date)

    def test_article_pub_status_change_updates_stream_item(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual(self.article.status, stream_item.status)
        self.article.status = 'D'
        self.article.save()
        stream_item = StreamItem.objects.get(pk=stream_item.id)
        self.assertEqual(self.article.status, stream_item.status)

    def test_stream_item_category_matches_article_category(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual(self.article.category, stream_item.category)

    def test_stream_item_title_matches_article_title(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual(self.article.title, u"%s" % stream_item)

    def test_stream_item_author_matches_article_author(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        self.assertEqual(self.article.author, stream_item.author)

    def test_article_category_change_updates_stream_item(self):
        category1 = Category.objects.create(name="Boo1", slug="boo1")
        category2 = Category.objects.create(name="Boo2", slug="boo2")
        article = Article.objects.create(title="Hey, a nice title",
                                         basename="testing-streamitem-ehh",
                                         category=category1,
                                         author=self.author,
                                         description="Duhscription")
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=article.id)
        self.assertEqual(article.category, stream_item.category)
        article.category = category2
        article.save()
        stream_item = StreamItem.objects.get(pk=stream_item.id)
        self.assertEqual(article.category, stream_item.category)

    def test_article_deletion_also_deletes_stream_item(self):
        StreamItem.objects.get(content_type=self.content_type,
                               object_id=self.article.id)
        self.article.delete()
        with self.assertRaises(StreamItem.DoesNotExist):
            StreamItem.objects.get(content_type=self.content_type,
                                   object_id=self.article.id)

    def test_non_existent_stream_item_after_article_delete(self):
        stream_item = StreamItem.objects.get(content_type=self.content_type,
                                             object_id=self.article.id)
        stream_item.delete()
        with self.assertRaises(StreamItem.DoesNotExist):
            self.article.delete()


class CategoryModelTestCase(TestCase):

    def test_category_name(self):
        category = Category.objects.create(name='Boo', slug='boo')
        self.assertEqual(category.name, 'Boo')
        self.assertEqual("%s" % category, 'Boo')


class SubCategoryModelTestCase(TestCase):

    def test_category_name(self):
        parent_category = Category.objects.create(name='Boo', slug='boo')
        sub_category = Category.objects.create(name='Radley', slug='radley',
                                               parent=parent_category)
        self.assertEqual(parent_category.name, 'Boo')
        self.assertEqual("%s" % parent_category, 'Boo')
        self.assertEqual(sub_category.name, 'Radley')
        self.assertEqual("%s" % sub_category, 'Radley')
        self.assertEqual(sub_category.parent, parent_category)


class CategoryPageTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category_slug = 'test-category'
        self.category_page_url =\
            self.get_category_page_url(category_slug=self.category_slug)

    def get_category_page_url(self, *args, **kwargs):
        return reverse('core_category_index', args=args, kwargs=kwargs)

    def test_page_load(self):
        Category.objects.create(slug=self.category_slug)
        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)

    def test_category_in_context(self):
        category = Category.objects.create(slug=self.category_slug)
        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.context.keys())
        self.assertEqual(response.context['category'].slug, category.slug)

    def test_parent_category_in_context_is_none(self):
        Category.objects.create(slug=self.category_slug)
        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('parent_category', response.context.keys())
        self.assertEqual(response.context['parent_category'], None)

    def test_unknown_slug(self):
        unknown_slug = "blahblah"
        bad_url = self.get_category_page_url(category_slug=unknown_slug)
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_stream_items_in_context(self):
        category = Category.objects.create(slug=self.category_slug)

        for i in range(settings.CORE_DEFAULT_INDEX_LENGTH):
            Article.objects.create(title="Testing StreamItem %d!" % i,
                                   basename="testing-si-%d" % i,
                                   category=category,
                                   status='P',
                                   author=self.author,
                                   description="Description %d" % i)

        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stream_items', response.context.keys())
        self.assertEqual(response.context['stream_items'].count(),
                         settings.CORE_DEFAULT_INDEX_LENGTH)


class TagPageTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category = Category.objects.create(slug='test-category')
        self.tag = Tag.objects.create(slug='test-tag', name='Test Tag')
        self.tag_page_url = self.get_tag_page_url(tag_slug=self.tag.slug)

    def get_tag_page_url(self, *args, **kwargs):
        return reverse('core_tag_index', args=args, kwargs=kwargs)

    def test_page_load(self):
        response = self.client.get(self.tag_page_url)
        self.assertEqual(response.status_code, 200)

    def test_tag_in_context(self):
        response = self.client.get(self.tag_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('tag', response.context.keys())
        self.assertEqual(response.context['tag'].slug, self.tag.slug)

    def test_unknown_slug(self):
        unknown_slug = "blahblah"
        bad_url = self.get_tag_page_url(tag_slug=unknown_slug)
        with self.assertRaises(Tag.DoesNotExist):
            self.client.get(bad_url)

    def test_stream_items_in_context(self):
        for i in range(settings.CORE_DEFAULT_INDEX_LENGTH):
            a = Article.objects.create(title="Testing StreamItem %d!" % i,
                                       basename="testing-si-%d" % i,
                                       category=self.category,
                                       status='P',
                                       author=self.author,
                                       description="Description %d" % i)
            a.tags.add(self.tag)
            print StreamItem.objects.filter(tags__in=[self.tag,])

        response = self.client.get(self.tag_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stream_items', response.context.keys())
        self.assertEqual(response.context['stream_items'].count(),
                         settings.CORE_DEFAULT_INDEX_LENGTH)


class SubCategoryPageTestCase(CategoryPageTestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category_slug = 'test-category'
        self.sub_category_slug = 'test-sub-category'
        self.category_page_url =\
            self.get_category_page_url(category_slug=self.category_slug,
                                       sub_category_slug=self.sub_category_slug)

    def test_page_load(self):
        parent = Category.objects.create(slug=self.category_slug)
        Category.objects.create(slug=self.sub_category_slug,
                                parent=parent)
        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)

    def test_category_in_context(self):
        parent = Category.objects.create(slug=self.category_slug)
        subcategory = Category.objects.create(slug=self.sub_category_slug,
                                              parent=parent)
        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.context.keys())
        self.assertEqual(response.context['category'].slug, subcategory.slug)
        self.assertEqual(response.context['category'].parent.slug,
                         subcategory.parent.slug)

    def test_parent_category_in_context(self):
        parent = Category.objects.create(slug=self.category_slug)
        Category.objects.create(slug=self.sub_category_slug,
                                parent=parent)
        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('parent_category', response.context.keys())
        self.assertEqual(response.context['parent_category'].slug,
                         parent.slug)

    def test_parent_category_in_context_is_none(self):
        """
        Placeholder override since we don't need to test this here.
        """
        pass

    def test_unknown_slug(self):
        bad_url = self.get_category_page_url(category_slug="blahblah",
                                             sub_category_slug="harhar")
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_stream_items_in_context(self):
        parent = Category.objects.create(slug=self.category_slug)
        sub_category = Category.objects.create(slug=self.sub_category_slug,
                                               parent=parent)

        for i in range(settings.CORE_DEFAULT_INDEX_LENGTH):
            Article.objects.create(title="Testing StreamItem %d!" % i,
                                   basename="testing-si-%d" % i,
                                   category=sub_category,
                                   status='P',
                                   author=self.author,
                                   description="Description %d" % i)

        response = self.client.get(self.category_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('stream_items', response.context.keys())
        self.assertEqual(response.context['stream_items'].count(),
                         settings.CORE_DEFAULT_INDEX_LENGTH)


class ArticlePageTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.coauthor = User.objects.create_user(username='justin',
                                                 email='bleh@meh.com',
                                                 password='******')
        self.category_slug = "exciting-content"
        self.category = Category.objects.create(slug=self.category_slug)
        self.basename = "share-with-your-friends"
        self.article = Article.objects.create(category=self.category,
                                              basename=self.basename,
                                              author=self.author)

    def test_article_page_load(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_article_in_context(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('content_item', response.context.keys())
        self.assertEqual(response.context['content_item'].basename,
                         self.article.basename)

    def test_category_in_context(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.context.keys())
        self.assertEqual(response.context['category'].slug, self.category.slug)

    def test_parent_category_in_context_is_none(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('parent_category', response.context.keys())
        self.assertEqual(response.context['parent_category'], None)

    def test_article_comments_included(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertTemplateUsed(response, template_name='comments.html')

    def test_article_comments_disabled(self):
        self.article.disable_comments = True
        self.article.save()
        response = self.client.get(self.article.get_absolute_url())
        self.assertTemplateNotUsed(response, template_name='comments.html')


class ArticleWithSubCategoryPageTestCase(TestCase):

    def test_coauthor(self):
        self.article.secondary_author = self.coauthor
        self.article.save()
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.context['content_item'].secondary_author, self.coauthor)

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category_slug = "exciting-content"
        self.sub_category_slug = "exciting-content-sub-category"
        self.basename = "share-with-your-friends-ok"
        self.article_url =\
            reverse('core_article',
                    kwargs={'category_slug': self.category_slug,
                            'sub_category_slug': self.sub_category_slug,
                            'basename': self.basename})

    def test_article_page_load(self):
        parent_category = Category.objects.create(slug=self.category_slug)
        sub_category = Category.objects.create(slug=self.sub_category_slug,
                                               parent=parent_category)
        Article.objects.create(category=sub_category, basename=self.basename,
                               author=self.author)
        response = self.client.get(self.article_url)
        self.assertEqual(response.status_code, 200)

    def test_article_context(self):
        parent_category = Category.objects.create(slug=self.category_slug)
        sub_category = Category.objects.create(slug=self.sub_category_slug,
                                               parent=parent_category)
        article = Article.objects.create(category=sub_category,
                                         basename=self.basename,
                                         author=self.author)
        response = self.client.get(self.article_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('content_item', response.context.keys())
        self.assertEqual(response.context['content_item'].basename,
                         article.basename)

    def test_category_context(self):
        parent_category = Category.objects.create(slug=self.category_slug)
        sub_category = Category.objects.create(slug=self.sub_category_slug,
                                               parent=parent_category)
        Article.objects.create(category=sub_category,
                               basename=self.basename,
                               author=self.author)
        response = self.client.get(self.article_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.context.keys())
        self.assertEqual(response.context['category'].slug, sub_category.slug)

    def test_parent_category_context(self):
        parent_category = Category.objects.create(slug=self.category_slug)
        sub_category = Category.objects.create(slug=self.sub_category_slug,
                                               parent=parent_category)
        Article.objects.create(category=sub_category,
                               basename=self.basename,
                               author=self.author)
        response = self.client.get(self.article_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('parent_category', response.context.keys())
        self.assertEqual(response.context['parent_category'].slug,
                         parent_category.slug)
