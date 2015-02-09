import csv
import os
import urllib2

from urlparse import urlparse

from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.utils.html import strip_tags
from django.utils.text import slugify

from asset_manager.models import Image
from core.models import Article, Category, LoopUser
from wordpress.models import Post, PostMeta


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.post_mapping_meta = {}
        self.parse_mapping()
        self.categories = list(Category.objects.all())
        published_posts = Post.objects.published()
        draft_posts = Post.objects.drafts()
        self.existing_images = Image.objects.all()
        for post in published_posts:
            self.create_article(post)

        for post in draft_posts:
            self.create_article(post, default_status='D')

    def parse_mapping(self):
        self.category_mapping = {}
        with open('%s/mapping.csv' % os.path.dirname(__file__), 'rb')\
             as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                parsed = urlparse(row['URL'])
                path = parsed.path.strip('/')
                print path
                self.category_mapping[path] = row['New Category']
                self.post_mapping_meta[path] = {'new_url': row['NEW URL'],
                                                'kill': row['KILL'],
                                                'redirect': row['REDIRECT'],
                                                'noindex': row['NOINDEX']}

    def create_article(self, post, default_status='P'):
        post_meta = PostMeta.objects.filter(post=post)
        meta_info = {'meta_description': '', 'subhead': ''}
        for meta in post_meta:
            if meta.key == 'post_subtitle':
                meta_info['subhead'] = meta.value
            elif meta.key == '_yoast_wpseo_metadesc':
                meta_info['meta_description'] = meta.value.replace('&nbsp;', ' ')
            elif meta.key == '_thumbnail_id':
                meta_info['thumbnail_id'] = meta.value

        if not meta_info['meta_description']:
            meta_info['meta_description'] = strip_tags(post.content)[:160]
        print post.title
        new_category = None
        if post.slug in self.category_mapping:
            for category in self.categories:
                if category.name == self.category_mapping[post.slug]:
                    new_category = category

        author, created = self.get_author_for_post(post)
        article = None

        if not new_category and default_status == 'D':
            new_category = Category.objects.get(name='Lifestyle')

        new_slug = post.slug
        if post.slug in self.post_mapping_meta\
           and self.post_mapping_meta[post.slug]['new_url']:
            new_slug = self.post_mapping_meta[post.slug]['new_url']


        try:
            article = Article.objects.get(basename=post.slug)
            article.title = post.title
            article.basename = new_slug
            article.category = new_category
            article.author = author
            article.subhead = meta_info['subhead']
            article.description = meta_info['meta_description'][:160]
            article.teaser = meta_info['meta_description']
            article.body = self.fix_body_content(post.content)
            article.status = default_status
            article.publication_date = post.post_date
            try:
                article.save()
            except Exception, e:
                print "EXCEPTION: %s barfed" % post.title
                print e
                return
        except Article.DoesNotExist:
            try:
                article = Article(title=post.title,
                                  basename=new_slug,
                                  category=new_category,
                                  author=author,
                                  subhead=meta_info['subhead'],
                                  description=meta_info['meta_description'][:160],
                                  teaser=meta_info['meta_description'],
                                  body=self.fix_body_content(post.content),
                                  status=default_status,
                                  publication_date=post.post_date)
                article.save()
            except Exception, e:
                print "EXCEPTION: %s barfed" % post.title
                print e
                return

        if 'thumbnail_id' in meta_info:
            image_asset = self.import_image(meta_info['thumbnail_id'])
            if image_asset:
                article.primary_image = image_asset
                article.save()
            else:
                print "NO IMAGE ASSET FOR %d" % post.id

        if post.slug in self.post_mapping_meta and\
           self.post_mapping_meta[post.slug]['noindex']:
            article.noindex = True

        if post.slug in self.post_mapping_meta and\
           self.post_mapping_meta[post.slug]['kill']:
            article.status = 'T'
            site = Site.objects.get_current()
            redirect, created = Redirect.objects.\
                                get_or_create(site=site,
                                              old_path="/%s/" % post.slug)
            if self.post_mapping_meta[post.slug]['redirect']:
                redirect.new_path = self.post_mapping_meta[post.slug]['redirect']
            else:
                redirect.new_path = article.category.get_absolute_url()
            redirect.save()
        else:
            if not article.status == 'D':
                site = Site.objects.get_current()
                redirect, created = Redirect.objects.\
                                    get_or_create(site=site,
                                                  old_path="/%s/" % post.slug)
                redirect.new_path = article.get_absolute_url()
                redirect.save()
        article.save()

    def fix_body_content(self, content):
        return u"<p>%s</p>" % content\
            .replace('\r\n\r\n', '</p>\r\n<p>')\
            .replace('<p><p>', '')\
            .replace('</p></p>', '')\
            .replace('<p>&nbsp;</p>', '')\
            .replace('reThink Israel', 'From the Grapevine')\
            .replace('ReThink Israel', 'From the Grapevine')\
            .replace('RTI', 'From the Grapevine')\
            .replace('reThink </strong><b>Israel', 'From the Grapevine')\

    def get_author_for_post(self, post):
        author, created = LoopUser.objects.get_or_create(
            username=u'%s' % post.author.username,
            email=u'%s' % post.author.email,
            first_name=post.author.display_name.split()[0],
            last_name=post.author.display_name.split()[1],
        )
        return author, created

    def import_image(self, image_post_id):
        image_post = Post.objects.get(pk=image_post_id)
        image_post_meta = PostMeta.objects.filter(post__id=image_post_id)
        image_basename = ''
        image_alt = ''
        image_caption = image_post.excerpt
        author, created = self.get_author_for_post(image_post)
        for meta in image_post_meta:
            if meta.key == '_wp_attached_file':
                image_basename = meta.value
            if meta.key == '_wp_attachment_image_alt':
                image_alt = meta.value
        image_fp = self.get_image_fp(image_basename)
        if not image_fp:
            return
        fp = File(image_fp)
        fp.name = image_basename
        new_asset = None
        for existing_image in self.existing_images:
            if existing_image.asset.name.find(fp.name) >= 0:
                existing_image.caption = image_caption
                existing_image.created_by = author
                existing_image.alt_text = image_alt[:255]
                existing_image.asset = fp
                existing_image.save()
                new_asset = existing_image
        if not new_asset:
            print "No match found for: ", image_caption
            new_asset = Image(caption=image_caption,
                              created_by=author,
                              alt_text=image_alt[:255],
                              asset=fp)
            new_asset.save()
        return new_asset

    def get_image_fp(self, image_path):
        if not image_path:
            return
        attempt1 = 'http://media.rti.mnn.com.s3.amazonaws.com/wp-content/uploads/%s' % image_path
        attempt2 = 'http://rethinkisrael.org/wp-content/uploads/%s' % image_path
        resp = None
        try:
            resp = urllib2.urlopen(attempt1)
            if not resp.code == 200:
                resp = urllib2.urlopen(attempt2)
        except:
            try:
                resp = urllib2.urlopen(attempt2)            
            except:
                print "FAILED FOR %s and %s" % (attempt1, attempt2)
        if resp:
            temp_file = NamedTemporaryFile(delete=True)
            temp_file.write(resp.fp.read())
            temp_file.flush()
            return temp_file

