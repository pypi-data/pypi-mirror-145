import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.views import redirect_to_login
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.http.response import Http404, HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from ckeditor.fields import RichTextField
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey
from simpel_themes.models import ModelTemplate
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase

from simpel_pages.managers import CategoryManager, PageManager, TagManager
from simpel_pages.utils import unique_slugify

from .routable import RouteResult
from .settings import pages_settings

logger = logging.getLogger(__name__)


class IndexView(ListView):
    page_template = None

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(self.page_template.render(context, self.request))


class Category(MPTTModel):

    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text=_(
            "Categories, unlike tags, can have a hierarchy. You might have a "
            "Jazz category, and under that have children categories for Bebop"
            " and Big Band. Totally optional."
        ),
    )
    thumbnail = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pagecategories",
    )
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_("Category Name"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
        max_length=80,
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_modified_at = models.DateTimeField(default=timezone.now)

    objects = CategoryManager()
    icon = "tag-outline"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        permissions = (
            ("import_category", _("Can import Category")),
            ("export_category", _("Can export Category")),
        )

    def __str__(self):
        return self.name

    @property
    def opts(self):
        return self.__class__._meta

    def get_absolute_url(self):
        return reverse("serve_category", kwargs={"slug": self.slug})

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent category cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


class Tag(TagBase):

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_modified_at = models.DateTimeField(default=timezone.now)
    icon = "tag-outline"

    objects = TagManager()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    @property
    def opts(self):
        return self._meta

    def get_absolute_url(self):
        return reverse("serve_tag", kwargs={"slug": self.slug})


class Page(MPTTModel):
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Last updated at"),
    )
    owner = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pages",
        verbose_name=_("Page Owner"),
    )
    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="childs",
        help_text=_(
            "Pages, unlike tags, can have a hierarchy. You might have a "
            "Index page, and under that have children pages for post"
            " and story. Totally optional."
        ),
    )
    title = models.CharField(
        _("title"),
        max_length=200,
    )
    category = TreeForeignKey(
        Category,
        related_name="pages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Category"),
    )
    tags = TaggableManager(
        through="TaggedPage",
        blank=True,
        related_name="pages",
        verbose_name=_("Tags"),
    )
    thumbnail = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="simpelpages",
    )
    content = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("Content"),
    )
    data = models.JSONField(null=True, blank=True)
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        max_length=255,
    )
    seo_title = models.CharField(
        _("SEO title"),
        null=True,
        blank=True,
        max_length=200,
    )
    seo_description = models.TextField(
        _("SEO description"),
        null=True,
        blank=True,
    )
    template = models.ForeignKey(
        ModelTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_templates",
        verbose_name=_("Template"),
    )
    url_path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    index = models.BooleanField(
        _("index"),
        default=False,
        help_text=_("Index page, contain child pages and not included in widgets."),
    )
    per_page = models.IntegerField(
        default=0,
        verbose_name=_("per page"),
        help_text=_("Number item per page, used only when index is True."),
    )
    live = models.BooleanField(
        _("live"),
        default=True,
    )
    allow_comments = models.BooleanField(
        _("allow comments"),
        default=False,
    )
    registration_required = models.BooleanField(
        _("registration required"),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    real_model = models.CharField(
        max_length=120,
        editable=False,
        null=True,
        blank=True,
    )
    readers = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="page_readers",
        verbose_name=_("Users who mark this page as read."),
    )
    bookmarks = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="bookmarks",
        verbose_name=_("Users who bookmark this page."),
    )
    visitor_count = models.IntegerField(default=0)

    objects = PageManager()

    def get_descendants(self, include_self=False):
        return super().get_descendants(include_self)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "%s" % self.title

    @property
    def opts(self):
        return self.get_real_model_class()._meta

    @property
    def specific(self):
        return self.get_real_instance()

    @property
    def page_type(self):
        return self.opts.verbose_name

    def get_related_by_category(self, number=5):
        return self.__class__.objects.get_related_by_category(self)[:number]

    def get_related_by_tags(self, number=5):
        return self.__class__.objects.get_related_by_tags(self)[:number]

    def has_permission(self):
        return True

    def route(self, request, path_components):
        if path_components:
            # request is for a child of this page
            child_slug = path_components[0]
            remaining_components = path_components[1:]

            try:
                subpage = self.get_children().get(slug=child_slug)
            except self.__class__.DoesNotExist:
                raise Http404

            return subpage.specific.route(request, remaining_components)

        else:
            # request is for this very page
            if self.live:
                return RouteResult(self)
            else:
                raise Http404

    def get_context_data(self, request, **kwargs):
        context = {
            "object": self,
            "page_title": self.seo_title or self.title,
            "page_description": self.seo_description or self.title,
        }
        context.update(kwargs)
        return context

    def get_template(self, request, *args, **kwargs):
        if not self.template:
            template = loader.get_template(pages_settings.DEFAULT_TEMPLATE)
        else:
            template = self.template.specific
        return template

    def serve_index(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        constructor = {
            "paginate_by": self.per_page or pages_settings.ITEM_PER_PAGE,
            "page_template": self.get_template(request),
            "extra_context": context,
            "queryset": self.childs.live(),
            "response_class": HttpResponse,
        }
        return IndexView.as_view(**constructor)(request, *args, **kwargs)

    def serve_page(self, request, *args, **kwargs):
        template = self.get_template(request, *args, **kwargs)
        context = self.get_context_data(request, **kwargs)
        return HttpResponse(template.render(context, request))

    def serve(self, request, *args, **kwargs):
        if self.registration_required and not request.user.is_authenticated:
            return redirect_to_login(request.path)
        if self.index:
            return self.serve_index(request, *args, **kwargs)
        return self.serve_page(request, *args, **kwargs)

    def set_url_path(self):
        if self.parent is not None:
            self.url_path = self.parent.url_path + self.slug + "/"
        else:
            self.url_path = ""
        return self.url_path

    def page_url(self, site=None, request=None):
        return reverse("serve_pages", args=(self.url_path,))

    def get_absolute_url(self, site=None, request=None):
        return self.page_url(site, request)

    def get_model_name(self):
        return "%s.%s" % (self.opts.app_label, self.opts.model_name)

    def get_real_model_class(self):
        """
        Return the real Model class related to objects.
        """
        try:
            return apps.get_model(self.real_model, require_ready=False)
        except Exception:
            if self.real_model is not None:
                logger.info("real model refers to model '%s' that has not been installed" % self.real_model)
            return self.__class__

    def get_real_instance(self):
        """Return the real page instance."""
        model = self.get_real_model_class()
        if model.__name__ == self.__class__.__name__:
            return self
        instance = model.objects.get(pk=self.id)
        return instance

    def get_root(self):
        root = super().get_root()
        instance = root.get_real_instance()
        return instance

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent page cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.slug:
            unique_slugify(self, self.title)
        if not self.real_model:
            self.real_model = self.get_model_name()
        self.set_url_path()
        return super().save(*args, **kwargs)


class RootPage(models.Model):
    site = models.OneToOneField(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rootpage",
        verbose_name=_("Site"),
    )
    page = models.OneToOneField(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        related_name="site",
        blank=True,
        verbose_name=_("Page"),
    )

    class Meta:
        verbose_name = _("Root")
        verbose_name_plural = _("Roots")
        swappable = "SIMPEL_PAGE_SITE_MODEL"

    def __str__(self):
        return "%s root Page" % self.site


class TaggedPage(TaggedItemBase):

    content_object = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="tagged_posts",
        db_index=True,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="tagged_pages",
        db_index=True,
    )

    class Meta:
        verbose_name = _("Tagged Page")
        verbose_name_plural = _("Tagged Pages")

    def __str__(self):
        return str(self.tag)


class Visitor(models.Model):
    ip = models.CharField(max_length=16, null=True)
    url = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    content_id = models.CharField(max_length=255, null=True)
    content = GenericForeignKey("content_type", "content_id")
