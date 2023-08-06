"""
    This module is largely inspired by django-rest-framework settings.
    This module provides the `settings` object, that is used to access
    app settings, checking for user settings first, then falling
    back to the defaults.
"""
from typing import Any, Dict

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

SETTINGS_DOC = "https://gitlab.com/sasriawesome/simpel_pages/-/wikis/"

SIMPEL_PAGES_DEFAULTS: Dict[str, Any] = {
    # Some settings here
    "APPEND_SLASH": True,
    "I18N_ENABLED": False,
    "VISITOR_SAVE": True,
    "VISITOR_CACHE_TIMEOUT": 60 * 60 * 24,
    "RELATED_PAGES_NUMBER": 5,
    "RELATED_PAGES_BY_TAGS_NUMBER": 5,
    "RELATED_PAGES_BY_CATEGORY_NUMBER": 5,
    "ITEM_PER_PAGE": 14,
    "CATEGORY_PER_PAGE": 14,
    "TAG_PER_PAGE": 14,
    "DEFAULT_TEMPLATE": "simpel_pages/default.html",
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = []

# List of settings that have been removed
REMOVED_SETTINGS = []


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    elif isinstance(val, dict):
        return {key: import_from_string(item, setting_name) for key, item in val.items()}
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for SIMPEL_PAGES setting '%s'. %s: %s." % (
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class AppSettings:
    """
    This module is largely inspired by django-rest-framework settings.
    This module provides the `pages_settings` object, that is used to access
    app settings, checking for user settings first, then falling
    back to the defaults.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or SIMPEL_PAGES_DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "SIMPEL_PAGES", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid SIMPEL_PAGES settings: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '%s' setting has been removed. Please refer to '%s' for available settings."
                    % (setting, SETTINGS_DOC)
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


pages_settings = AppSettings(None, SIMPEL_PAGES_DEFAULTS, IMPORT_STRINGS)


def reload_pages_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "SIMPEL_PAGES":
        pages_settings.reload()


setting_changed.connect(reload_pages_settings)
