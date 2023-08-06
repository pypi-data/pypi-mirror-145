from django.db import models
from django.utils import timezone

from mptt.managers import TreeManager, TreeQuerySet


class TagManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("tagged_pages")
        count = models.Count("tagged_pages", distinct=True)
        return qs.prefetch_related("tagged_pages").annotate(tagged_count=count).order_by("name")

    def popular(self):
        return self.get_queryset().order_by("-tagged_count")


class CategoryManager(TreeManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related("parent")


class PageQueryset(TreeQuerySet):
    def as_manager(cls):
        # Address the circular dependency between `Queryset` and `Manager`.
        from simpel_pages.managers import PageManager

        manager = PageManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)

    def live(self):
        return self.filter(live=True)

    def _get_real_model_name(self, model):
        if issubclass(model, models.Model):
            opts = model._meta
            model_name = "%s.%s" % (opts.app_label, opts.model_name)
        if isinstance(model, (str,)):
            model_name = model
        return model_name

    def instance_of(self, model):
        if isinstance(model, (list, set, tuple)):
            models = [m for m in self._get_real_model_name(model)]
        else:
            models = [self._get_real_model_name(model)]
        return self.filter(real_model__in=models)


class PageManager(models.Manager.from_queryset(PageQueryset), TreeManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related("parent")

    def get_related_by_category(self, obj, tree=True, full=False):
        qs = self.get_queryset()
        cat = obj.category
        if cat is None:
            return qs.none()
        if tree:
            cats = [cat]
            if full:
                cats += list(cat.get_descendants())
            else:
                cats += list(cat.children.all())
        else:
            cats = [cat]
        slugs = [c.slug for c in cats]
        qs = self.get_queryset()
        return qs.filter(category__slug__in=slugs).exclude(pk=obj.id).live()

    def get_related_by_tags(self, obj):
        tags = obj.tags.all()
        slugs = [tag.slug for tag in tags]
        qs = self.get_queryset()
        return qs.filter(tags__slug__in=slugs).distinct().exclude(pk=obj.id).live()

    def get_most_viewed(self, from_date=None, to_date=None):
        qs = self.get_queryset()
        if to_date is None:
            to_date = timezone.now()
        return qs.filter(created_at__range=[from_date, to_date])
