from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, cache_control
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView

from .models import (Article, Blog, Category, LoopUser, PhotoBlog,
                     PhotoOfTheDay, Slideshow, StreamItem, Tag,
                     TipsList, Infographic)
from .utils import get_author_from_slug, get_categories


class CacheControlMixin(View):

    @method_decorator(cache_control(max_age=settings.CACHE_CONTROL_MAX_AGE))
    @method_decorator(cache_page(settings.CACHE_CONTROL_MAX_AGE))
    def dispatch(self, *args, **kwargs):
        return super(CacheControlMixin, self).dispatch(*args, **kwargs)


class StreamIndex(TemplateView, CacheControlMixin):
    template_name = 'home.html'
    queryset = StreamItem.published.select_related('category', 'content_type')

    def get(self, request, *args, **kwargs):
        """
        If the requested page is page 1, redirect to the initial index page.
        This prevents duplicate URLs representing the initial page of content
        for a given index stream.
        """
        if 'page_num' in kwargs and kwargs['page_num'] is not None:
            if int(kwargs['page_num']) == 1:
                return HttpResponsePermanentRedirect(self.initial_index_view())
        return super(StreamIndex, self).get(request, *args, **kwargs)

    def initial_index_view(self):
        return reverse_lazy('core_home')

    def get_context_data(self, page_num=None):
        """
        Collect the appropriate stream items and return them along
        with the pagination object.
        """
        page_num = self.validate_page_arg(page_num)
        stream_items = self.get_objects()
        pagination_obj = self.paginate_items(stream_items, page_num)
        return {'pagination_obj': pagination_obj,
                'stream_items': pagination_obj.object_list}

    def get_objects(self):
        """
        By default, returns all published StreamItems. For subclasses of
        StreamIndex, this method should be overridden as necessary to provide
        the proper subset of StreamItems.
        """
        return self.queryset

    def paginate_items(self, stream_items, page_num):
        """
        Return stream_items according to the specified page number,
        calling fetch_generic_relations to reduce DB queries when fetching
        content_objects.
        """
        paginator = Paginator(stream_items, settings.CORE_DEFAULT_INDEX_LENGTH)
        try:
            stream_items = paginator.page(page_num)
        except (EmptyPage, InvalidPage):
            raise Http404
        return stream_items

    def validate_page_arg(self, page_num):
        """
        Make sure page_num has a page_num.
        """
        if page_num is None:
            page_num = 1
        return page_num


class CategoryStreamIndex(StreamIndex):
    template_name = 'category_index.html'

    def get_context_data(self, category_slug,
                         sub_category_slug, page_num=None):
        try:
            (self.primary_category,
             self.parent_category) = get_categories(category_slug,
                                                    sub_category_slug)
        except Category.DoesNotExist:
            raise Http404
        self.featured_items = []
        context = super(CategoryStreamIndex, self).get_context_data(page_num)
        context['category'] = self.primary_category
        context['parent_category'] = self.parent_category
        context['featured_items'] = self.featured_items
        return context

    def initial_index_view(self):
        return reverse_lazy('core_category_index',
                            kwargs={'category_slug': self.kwargs['category_slug']})

    def get_objects(self):
        """
        By default, returns all published StreamItems. For subclasses of
        StreamIndex, this method should be overridden as necessary to provide
        the proper subset of StreamItems.
        """
        qs = self.queryset.filter(category=self.primary_category)
        featured_ids = []
        featured_items = self.primary_category.get_featured_content()
        if featured_items:
            self.featured_items = featured_items
            featured_ids.append(featured_items[0].stream_item.id)
        if featured_ids:
            qs = qs.exclude(id__in=featured_ids)
        return qs


class TagStreamIndex(StreamIndex):
    template_name = 'tag_index.html'

    def get_context_data(self, tag_slug, page_num=None):
        self.tag = Tag.objects.get(slug=tag_slug)
        self.featured_items = []
        context = super(TagStreamIndex, self).get_context_data(page_num)
        context['tag'] = self.tag
        context['featured_items'] = self.featured_items
        return context

    def initial_index_view(self):
        return reverse_lazy('core_tag_index',
                            kwargs={'tag_slug': self.kwargs['tag_slug']})

    def get_objects(self):
        """
        By default, returns all published StreamItems. For subclasses of
        StreamIndex, this method should be overridden as necessary to provide
        the proper subset of StreamItems.
        """
        qs = self.queryset.filter(tags__in=[self.tag,])
        featured_ids = []
        featured_items = self.tag.get_featured_content()
        if featured_items:
            self.featured_items = featured_items
            featured_ids.append(featured_items[0].stream_item.id)
        if featured_ids:
            qs = qs.exclude(id__in=featured_ids)
        return qs


class AuthorStreamIndex(StreamIndex):
    template_name = 'author_index.html'

    def get_context_data(self, author_slug, page_num=None):
        self.author = get_author_from_slug(author_slug)
        context = super(AuthorStreamIndex, self).get_context_data(page_num)
        context['author'] = self.author
        return context

    def initial_index_view(self):
        return reverse_lazy('core_author_index',
                            kwargs={'author_slug': self.kwargs['author_slug']})

    def get_objects(self):
        """
        By default, returns all published StreamItems. For subclasses of
        StreamIndex, this method should be overridden as necessary to provide
        the proper subset of StreamItems.
        """
        return self.queryset.filter(Q(author=self.author)\
                                    | Q(secondary_author=self.author))


class ContentDetailView(DetailView, CacheControlMixin):

    context_object_name = 'content_item'
    primary_category = None
    parent_category = None
    require_appended_slash = False

    def get(self, request, *args, **kwargs):
        """
        If require_appended_slash is True and none is found,
        redirect to the path with a slash appended.
        """
        if not request.path.endswith('/') and self.require_appended_slash:
            return HttpResponsePermanentRedirect('%s/' % request.path)
        return super(ContentDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ContentDetailView, self).get_queryset()
        if self.request.user.is_staff or self.request.GET.get('preview'):
            queryset = self.model.objects.all()
        return queryset

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        try:
            self.primary_category, \
                self.parent_category = get_categories(self.kwargs.get('category_slug'),
                                                      self.kwargs.get('sub_category_slug'))
            basename = self.kwargs.get('basename')
        except Category.DoesNotExist:
            raise Http404
        try:
            content_obj = queryset.get(category=self.primary_category,
                                       basename=basename)
        except self.model.DoesNotExist:
            raise Http404
        return content_obj

    def get_context_data(self, **kwargs):
        context = super(ContentDetailView, self).get_context_data(**kwargs)
        context.update({
            'category': self.primary_category,
            'parent_category': self.parent_category,
        })

        if self.object.status != 'P':
            messages.add_message(self.request,
                                 messages.WARNING,
                                 'You are currently viewing this content in ' + \
                                 'Preview Mode, this content is not live.')
        return context


class ArticleView(ContentDetailView):
    model = Article
    template_name = 'article.html'

    queryset = Article.published.all()


class BlogView(ContentDetailView):
    model = Blog
    template_name = 'article.html'
    queryset = Blog.published.all()

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context.update({
            'disclaimer': settings.BLOG_DISCLAIMER,
        })
        return context


class InfographicView(ContentDetailView):
    model = Infographic
    template_name = 'infographic.html'

    queryset = Infographic.published.all()


class PhotoBlogView(ContentDetailView):
    model = PhotoBlog
    template_name = 'photo_blog.html'

    queryset = PhotoBlog.published.all()


class TipsListView(ContentDetailView):
    model = TipsList
    template_name = 'tips_list.html'

    queryset = TipsList.published.all()


class PhotoOfTheDayView(ContentDetailView):
    model = PhotoOfTheDay
    require_appended_slash = True
    template_name = 'photo_of_the_day.html'

    queryset = PhotoOfTheDay.published.all()

    def get_context_data(self, **kwargs):
        context = super(PhotoOfTheDayView, self).get_context_data(**kwargs)
        next_pod = None
        prev_pod = None
        todays_pod = PhotoOfTheDay.published.first()

        try:
            next_pod = self.object.get_next_by_publication_date(status="P")
        except PhotoOfTheDay.DoesNotExist:
            pass

        try:
            prev_pod = self.object.get_previous_by_publication_date(status="P")
        except PhotoOfTheDay.DoesNotExist:
            pass
        
        qs_count = self.queryset.count()
        try:
            row_number = list(self.queryset).index(self.object)
        except ValueError:
            row_number = -1

        context.update({
            'next_pod': next_pod,
            'prev_pod': prev_pod,
            'todays_pod': todays_pod,
            'total_pod_count': qs_count,
            'x_of_y': row_number + 1
        })

        return context


class SlideShowView(ContentDetailView):
    model = Slideshow
    template_name = 'slide.html'
    context_object_name = 'content_item'

    def get_queryset(self):
        queryset = super(SlideShowView, self).get_queryset()
        return queryset.prefetch_related('slide_set')

    def get_object(self, queryset=None):
        slideshow = super(SlideShowView, self).get_object(queryset)
        return slideshow

    def get_context_data(self, **kwargs):
        context = super(SlideShowView, self).get_context_data(**kwargs)

        # Set page_num, accounting for 3 conditions:
        # 1. self.kwargs has no 'page_num' key
        # 2. self.kwargs['page_num'] exists and is None
        # 3. self.kwargs['page_num'] exists and has a value
        page_num = self.kwargs.get('page_num', 1) or 1
        current_slide = None
        previous_slide = None
        next_slide = None

        # page_num will be 1-based, so subtract one to index into the slide_set
        page_num = int(page_num) - 1
        slides = self.object.slide_set.all()

        if page_num < 0 or page_num > (len(slides) - 1):
            raise Http404

        current_slide = slides[page_num]

        if current_slide.order > 0:
            previous_slide = slides[current_slide.order - 1]

        if current_slide.order < (len(slides) - 1):
            next_slide = slides[current_slide.order + 1]

        context.update({
            'current_slide': current_slide,
            'previous_slide': previous_slide,
            'next_slide': next_slide,
        })

        return context


class ComingSoonView(TemplateView):
    template_name = 'coming_soon.html'


class RSSLandingPageView(TemplateView):
    template_name = 'rss_landing.html'

    def get_context_data(self, **kwargs):
        context = super(RSSLandingPageView, self).get_context_data(**kwargs)
        published_authors = StreamItem.published\
                                      .order_by('author__id')\
                                      .values_list('author', flat=True)\
                                      .distinct()
        context['authors'] = LoopUser.objects.filter(id__in=published_authors)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context
