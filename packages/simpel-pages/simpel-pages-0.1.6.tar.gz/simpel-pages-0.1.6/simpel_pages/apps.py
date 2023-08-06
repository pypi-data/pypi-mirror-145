from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class SimpelPagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "simpel_pages"
    icon = "page-next-outline"
    label = "simpel_pages"
    verbose_name = _("Pages")

    def ready(self):
        post_migrate.connect(init_app, sender=self)


def init_app(**kwargs):
    pass
