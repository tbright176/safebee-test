import copy
import reversion

from suit.admin import SortableStackedInline
from suit.widgets import SuitSplitDateTimeWidget
from suit_redactor.widgets import RedactorWidget

from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected as delete_selected_orig
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from asset_manager.widgets import ImageAssetWidget
from .admin_forms import (ArticleAdminForm, ContentAdminForm,
                          PhotoOfTheDayAdminForm, SlideAdminForm,
                          LoopUserChangeForm, LoopUserCreationForm,
                          SlideInlineFormset)
from .models import (Article, Category,Infographic,  LoopUser, PhotoOfTheDay,
                     Photo, PhotoBlog, Slideshow, Slide, StreamItem,
                     Tag, TipsList, TipsListItem, RelatedItem)


class LoopUserAdmin(UserAdmin):
    form = LoopUserChangeForm
    add_form = LoopUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        ('Bio Info', {'fields': ('title', 'bio', 'profile_image')}),
        ('Social', {'fields': ('google_plus_profile_url', 'twitter')}),
        ('About Us Inclusion', {'fields': ('include_on_about_page', 'inclusion_ordering')}),
    )
    ordering = ('first_name', 'last_name')


class ViewOnSiteMixin(object):
    change_form_template = 'admin/content_change_form.html'


class LoopModelAdmin(ViewOnSiteMixin, admin.ModelAdmin):
    pass


class RelatedInline(SortableStackedInline, GenericStackedInline):
    model = RelatedItem
    extra = 0
    raw_id_fields = ('image', 'stream_item')

    class Media:
        js = ('core/admin/related_stream_popup.js',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(RelatedInline, self).formfield_for_foreignkey(db_field,
                                                                   request,
                                                                   **kwargs)


class FeaturedItemInline(RelatedInline):
    verbose_name = 'Featured Item'
    verbose_name_plural = 'Featured Item'


class ContentAdmin(ViewOnSiteMixin, reversion.VersionAdmin):
    date_hierarchy = 'publication_date'
    form = ContentAdminForm
    formfield_overrides = {
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
    }
    fieldsets = [
        ('General', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('title', 'basename', 'subhead', 'description',
                       'teaser', 'tags',)
        }),
        ('Images', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('primary_image', 'social_image', 'promo_image'),
        }),
        ('Publishing Settings', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('author', 'secondary_author', 'category',
                       'publication_date', 'status', 'notes')
        }),
        ('Page Settings', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('page_title', 'disable_comments',)
        }),
        ('Meta/SEO', {
            'classes': ('suit-tab suit-tab-meta',),
            'fields': ('canonical_url', 'news_keywords', 'enable_standout_tag',
                       'noodp_noydir', 'nofollow', 'noindex')
        }),
        ('Promotional', {
            'classes': ('suit-tab suit-tab-promo',),
            'fields': ('exclude_from_rss', 'exclude_from_newsletter_rss',
                       'exclude_from_twitter', 'exclude_from_sitemap',
                       'exclude_from_most_popular')
        }),
    ]
    filter_horizontal = ('tags',)
    list_display = ('title', 'status', 'author', 'category',
                    'publication_date', 'view_obj')
    list_filter = ('status', 'author', 'category', 'disable_comments')
    prepopulated_fields = {"basename": ("title",)}
    raw_id_fields = ('primary_image', 'social_image', 'promo_image',)
    search_fields = ['title', 'basename', 'id']
    suit_form_tabs = (('general', 'General'), ('meta', 'Meta/SEO'),
                      ('promo', 'Promotional'))

    actions = ['delete_selected', 'make_moderate', 'make_published']
    actions_on_top = True

    inlines = [
        RelatedInline,
    ]

    class Media:
        css = {
            'all': ('core/admin/input.css',)
        }
        js = ('asset_manager/redactor.js', 'asset_manager/fullscreen.js',)

    def suit_row_attributes(self, obj, request):
        status_class = {
            'D': 'info',
            'M': 'warning',
            'P': None,
            'S': 'success',
        }.get(obj.status)
        if status_class:
            return {'class': status_class, 'data': u"%s" % obj}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ('primary_image', 'social_image', 'promo_image'):
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(ContentAdmin, self).formfield_for_foreignkey(db_field,
                                                                  request,
                                                                  **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            if Group.objects.get(name="Moderated Writers") in\
                    request.user.groups.all():
                kwargs['choices'] = (
                    ('D', 'Draft'),
                    ('M', 'Submit for Moderation'))
        return super(ContentAdmin, self)\
            .formfield_for_choice_field(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        can_delete = super(ContentAdmin, self).has_delete_permission(request, obj)
        if obj and obj.status == 'P':
            return False
        return can_delete

    def delete_selected(self, request, queryset):
        queryset = queryset.exclude(status='P')
        if queryset.count() < 1:
            msg = _("You must select non-published content to delete.")
            self.message_user(request, msg, messages.WARNING)
            return None
        return delete_selected_orig(self, request, queryset)
    delete_selected.short_description = 'Delete selected content'

    def make_published(self, request, queryset):
        queryset.update(status='P')
    make_published.short_description = "Mark selected stories as Published"

    def make_moderate(self, request, queryset):
        queryset.update(status='M')
    make_moderate.short_description = "Mark selected stories as Moderate"

    def get_actions(self, request):
        actions = super(ContentAdmin, self).get_actions(request)
        if not request.user.is_superuser and\
           not Group.objects.get(name="Editors") in request.user.groups.all():
            actions_to_remove = ['make_moderate', 'make_published']
            for action in actions_to_remove:
                if action in actions:
                    del actions[action]
        return actions

    def get_view_on_site_url(self, obj=None):
        if obj is None or not self.view_on_site:
            return None
        if obj and hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url() + "?preview=true"

        return super(ContentAdmin, self).get_view_on_site_url(obj)

    def view_obj(self, obj=None):
        if obj.status == 'P':
            content_type = ContentType.objects.get_for_model(obj)
            url = reverse('admin:view_on_site',
                          kwargs={'content_type_id': content_type.id,
                                  'object_id': obj.id})
        else:
            try:
                url = self.get_view_on_site_url(obj)
            except:
                url = ''
        return """<a href="%s" target="_blank"><i class="icon-share"></i></a>""" % url
    view_obj.short_description = "View"
    view_obj.allow_tags = True


class ArticleAdmin(ContentAdmin):
    form = ArticleAdminForm
    search_fields = ['title', 'basename', 'id', 'body']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleAdmin, self).get_fieldsets(request, obj)
        fieldsets_copy = copy.deepcopy(fieldsets)
        if len(fieldsets_copy) > 2:
            if not fieldsets_copy[1][0] == 'Body':
                body_fieldset = ('Body', {
                    'classes': ('full-width', 'wide',
                                'suit-tab suit-tab-general'),
                    'fields': ('body',)
                })
                fieldsets_copy.insert(1, body_fieldset)
                image_fields = list(fieldsets_copy[2][1]['fields'])
                image_fields.insert(1, 'primary_image_caption_override')
                fieldsets_copy[2][1]['fields'] = image_fields
        return fieldsets_copy


class InfographicAdmin(ContentAdmin):
    form = ArticleAdminForm
    search_fields = ['title', 'basename', 'id', 'body']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(InfographicAdmin, self).get_fieldsets(request, obj)
        fieldsets_copy = copy.deepcopy(fieldsets)
        if len(fieldsets_copy) > 2:
            if not fieldsets_copy[1][0] == 'Body':
                body_fieldset = ('Body', {
                    'classes': ('full-width', 'wide',
                                'suit-tab suit-tab-general'),
                    'fields': ('body',)
                })
                fieldsets_copy.insert(1, body_fieldset)
        return fieldsets_copy


class TaxonomyAdmin(ViewOnSiteMixin, reversion.VersionAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')
    inlines = [
        FeaturedItemInline,
    ]


class CategoryAdmin(TaxonomyAdmin):
    pass


class SlideInline(SortableStackedInline):
    extra = 0
    form = SlideAdminForm
    formset = SlideInlineFormset
    model = Slide
    sortable = 'order'
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['title', 'image', 'caption', 'order'],
        }),
    ]
    formfield_overrides = {
        models.TextField: {'widget':\
                           RedactorWidget(editor_options=\
                                          {'minHeight': '300',})},
    }
    raw_id_fields = ('image',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(ContentAdmin, self).formfield_for_foreignkey(db_field,
                                                                  request,
                                                                  **kwargs)


class SlideshowAdmin(ContentAdmin):
    inlines = [SlideInline,]

    def get_queryset(self, request):
        return super(SlideshowAdmin, self)\
            .get_queryset(request).prefetch_related('slide_set')


class PhotoOfTheDayAdmin(ContentAdmin):
    form = PhotoOfTheDayAdminForm
    search_fields = ['title', 'subtitle', 'id', 'caption']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(PhotoOfTheDayAdmin, self).get_fieldsets(request, obj)
        fieldsets_copy = copy.deepcopy(fieldsets)
        if len(fieldsets_copy) > 2:
            if not fieldsets_copy[1][0] == 'Photo of the Day Content':
                body_fieldset = ('Photo of the Day Content', {
                    'classes': ('suit-tab suit-tab-general',),
                    'fields': ('subtitle', 'caption',)
                })
                fieldsets_copy.insert(2, body_fieldset)
        return fieldsets_copy


class PhotoInline(SlideInline):
    extra = 0
    model = Photo


class PhotoBlogAdmin(ContentAdmin):
    inlines = [PhotoInline,]

    def get_queryset(self, request):
        return super(PhotoBlogAdmin, self)\
            .get_queryset(request).prefetch_related('photo_set')


class TipsListItemInline(SlideInline):
    extra = 0
    model = TipsListItem


class TipsListAdmin(ContentAdmin):
    inlines = [TipsListItemInline,]

    def get_queryset(self, request):
        return super(TipsListAdmin, self)\
            .get_queryset(request).prefetch_related('tipslistitem_set')


class StreamItemAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'author', 'category', 'status',)
    list_filter = ('status', 'author', 'category',)
    search_fields = ['title', 'id']

    def has_add_permission(self, request):
        return False


class TagAdmin(TaxonomyAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Infographic, InfographicAdmin)
admin.site.register(PhotoBlog, PhotoBlogAdmin)
admin.site.register(PhotoOfTheDay, PhotoOfTheDayAdmin)
admin.site.register(LoopUser, LoopUserAdmin)
admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(StreamItem, StreamItemAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TipsList, TipsListAdmin)
