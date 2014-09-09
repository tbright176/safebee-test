from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from core.admin_forms import ContentAdminForm
from core.models import Article, Category
from core.templatetags.core import site_title_string

User = get_user_model()


class WebDriverBaseTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(WebDriverBaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(WebDriverBaseTestCase, cls).tearDownClass()


class HomePageFunctionalTestCase(WebDriverBaseTestCase):

    def test_page_title(self):
        current_site = Site.objects.get_current()
        self.selenium.get(self.live_server_url)
        self.assertEqual(self.selenium.title, current_site.name)

    def test_noodp_noydir_default(self):
        self.selenium.get(self.live_server_url)
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='robots' and"
                                       "@content='NOODP,NOYDIR']"))
        except NoSuchElementException:
            found = self.selenium\
                        .find_element_by_xpath("//meta[@name='robots']")
            self.fail(("The meta robots tag matching xpath could not be found. "
                       "Found content: %s" % found.get_attribute('content')))


class CategoryIndexPageFunctionalTestCase(WebDriverBaseTestCase):

    def test_page_title(self):
        category = Category.objects.create(name='Test Category',
                                           slug='test-category')
        url = reverse('core_category_index',
                      kwargs={'category_slug': category.slug})
        self.selenium.get("%s%s" % (self.live_server_url, url))
        self.assertEqual(self.selenium.title, "%s %s" % (category.name,
                                                         site_title_string()))


class SubCategoryIndexPageFunctionalTestCase(WebDriverBaseTestCase):

    def test_page_title(self):
        parent_category = Category.objects.create(name='Boo', slug='boo')
        category = Category.objects.create(name='Radley',
                                           slug='radley',
                                           parent=parent_category)
        url = reverse('core_category_index',
                      kwargs={'category_slug': parent_category.slug,
                              'sub_category_slug': category.slug})
        self.selenium.get("%s%s" % (self.live_server_url, url))
        self.assertEqual(self.selenium.title, "%s %s" % (category.name,
                                                         site_title_string()))


class SlideshowFunctionalTestCase(WebDriverBaseTestCase):
    pass


class ArticlePageFunctionalTestCase(WebDriverBaseTestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
        self.author = User.objects.create_user(username='ben',
                                               email='blah@blah.com',
                                               password='123456')
        self.category = Category.objects.create(slug='test-category')
        self.article = Article.objects.create(basename='test-article-basename',
                                              category=self.category,
                                              title="This is the title!",
                                              author=self.author)

    def test_article_title(self):
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        self.assertEqual(self.selenium.title, "%s %s"\
                         % (self.article.title, site_title_string()))
        self.assertEqual(self.selenium.title, "%s %s"\
                         % (self.article, site_title_string()))

    def test_article_title_with_custom_page_title(self):
        self.article.page_title = "Hey, It's a Custom Title!"
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        self.assertEqual(self.selenium.title, "%s %s"\
                         % (self.article.get_title(), site_title_string()))

    def test_article_h1_title_exists(self):
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        heading1 = self.selenium.find_element_by_tag_name('h1')
        self.assertEqual(heading1.text, self.article.title)

    def test_article_rel_canonical_exists(self):
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium.find_element_by_xpath("//link[@rel='canonical' and @href='%s']" % self.article.get_canonical_url())
        except NoSuchElementException:
            self.fail("The rel_canonical tag could not be found.")

    def test_article_noodp_noydir_default(self):
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='robots' and"
                                       "@content='NOODP,NOYDIR']"))
        except NoSuchElementException:
            found = self.selenium\
                        .find_element_by_xpath("//meta[@name='robots']")
            self.fail(("The meta robots tag matching xpath could not be found. "
                       "Found content: %s" % found.get_attribute('content')))

    def test_article_noodp_noydir_and_nofollow(self):
        self.article.nofollow = True
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='robots' and"
                                       "@content='NOODP,NOYDIR,NOFOLLOW']"))
        except NoSuchElementException:
            found = self.selenium\
                        .find_element_by_xpath("//meta[@name='robots']")
            self.fail(("The meta robots tag matching xpath could not be found. "
                       "Found content: %s" % found.get_attribute('content')))

    def test_article_noodp_noydir_and_nofollow_and_noindex(self):
        self.article.nofollow = True
        self.article.noindex = True
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='robots' and"
                                       "@content='NOODP,NOYDIR,NOFOLLOW,NOINDEX']"))
        except NoSuchElementException:
            found = self.selenium\
                        .find_element_by_xpath("//meta[@name='robots']")
            self.fail(("The meta robots tag matching xpath could not be found. "
                       "Found content: %s" % found.get_attribute('content')))

    def test_article_disable_noodp_noydir(self):
        self.article.noodp_noydir = False
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        with self.assertRaises(NoSuchElementException):
            self.selenium\
                .find_element_by_xpath("//meta[@name='robots']")

    def test_article_disable_noodp_noydir_enable_nofollow(self):
        self.article.noodp_noydir = False
        self.article.nofollow = True
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='robots' and"
                                       "@content='NOFOLLOW']"))
        except NoSuchElementException:
            found = self.selenium\
                        .find_element_by_xpath("//meta[@name='robots']")
            self.fail(("The meta robots tag matching xpath could not be found. "
                       "Found content: %s" % found.get_attribute('content')))

    def test_article_disable_noodp_noydir_enable_noindex(self):
        self.article.noodp_noydir = False
        self.article.noindex = True
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='robots' and"
                                       "@content='NOINDEX']"))
        except NoSuchElementException:
            found = self.selenium\
                        .find_element_by_xpath("//meta[@name='robots']")
            self.fail(("The meta robots tag matching xpath could not be found. "
                       "Found content: %s" % found.get_attribute('content')))

    def test_article_disable_noodp_noydir_enable_nofollow_enable_noindex(self):
        self.article.noodp_noydir = False
        self.article.nofollow = True
        self.article.noindex = True
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='robots' and"
                                       "@content='NOFOLLOW,NOINDEX']"))
        except NoSuchElementException:
            found = self.selenium\
                        .find_element_by_xpath("//meta[@name='robots']")
            self.fail(("The meta robots tag matching xpath could not be found. "
                       "Found content: %s" % found.get_attribute('content')))

    def test_article_news_keywords(self):
        content_data = {'author': self.article.author.id,
                        'title': self.article.title,
                        'basename': self.article.basename,
                        'category': self.article.category.id,
                        'description': "This is the description",
                        'status': self.article.status,
                        'publication_date': self.article.publication_date}
        content_data['news_keywords'] = 'hey1, hey2, hey 4, yeah kinda'
        form = ContentAdminForm(content_data, instance=self.article)
        if form.is_valid():
            form.save()
        else:
            self.fail("Form was invalid due to these errors: %s" % form.errors)
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium\
                .find_element_by_xpath(("//meta[@name='news_keywords' and "
                                        "@content='hey1,hey2,hey 4,yeah"
                                        " kinda']"))
        except NoSuchElementException:
            found = self.selenium.find_element_by_xpath(("//meta[@name="
                                                         "'news_keywords']"))
            self.fail("Could not find the news_keywords meta tag. Found: %s"\
                      % found.get_attribute('content'))

    def test_article_description(self):
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium.find_element_by_xpath(("//meta[@name='description' "
                                                 "and @content='%s']" % self.article.description))
        except NoSuchElementException:
            self.fail("Could not find expected meta description tag.")

    def test_article_subhead(self):
        self.article.subhead = "This is the subhead."
        self.article.save()
        self.selenium.get("%s%s" % (self.live_server_url,
                                    self.article.get_absolute_url()))
        try:
            self.selenium.find_element_by_xpath(("//p[@class='subhead' "
                                                 "and contains(., '%s')]" % self.article.subhead))
        except NoSuchElementException:
            self.fail("Could not find expected article subhead.")

    #def test_article_meta_fb_app_id(self):
    #    current_site = Site.objects.get_current()
    #    self.selenium.get("%s%s" % (self.live_server_url,
    #                                self.article.get_absolute_url()))
    #    try:
    #        self.selenium\
    #            .find_element_by_xpath(("//meta[@property='fb:app_id' "
    #                                    "and @content='%s']" % current_site.fb_app_id))
    #    except NoSuchElementException:
    #        self.fail("Could not find expected meta description tag.")

    #def test_article_og_image(self):
    #    current_site = Site.objects.get_current()
    #    image = Image.objects.get(pk=1)
    #    self.article.primary_image = image
    #    self.article.save()
    #    self.selenium.get("%s%s" % (self.live_server_url,
    #                                self.article.get_absolute_url()))
    #    try:
    #        self.selenium\
    #            .find_element_by_xpath(("//meta[@property='og:image' "
    #                                    "and @content='http://%s%s']" % (current_site.domain, self.article.primary_image.asset.url)))
    #    except NoSuchElementException:
    #        self.fail("Could not find expected og:image tag")
