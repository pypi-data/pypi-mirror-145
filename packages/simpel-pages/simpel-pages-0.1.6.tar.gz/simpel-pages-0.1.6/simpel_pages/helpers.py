import hashlib

from django.core.cache import cache

from simpel_pages.utils import get_ip

from .models import Visitor
from .settings import pages_settings


def log_visitor(request, status_code=None, content=None):
    ip = get_ip(request)
    url = request.build_absolute_uri()
    cache_key = "Visitor:%s" % hashlib.sha1(f"{ip}-{url}".encode("utf-8")).hexdigest()
    timeout = pages_settings.VISITOR_CACHE_TIMEOUT
    last_visit = cache.get(cache_key)
    if not last_visit:
        if pages_settings.VISITOR_SAVE:
            referrer = request.META.get("HTTP_REFERER")
            data = {
                "ip": ip,
                "url": url,
                "path": request.get_full_path(),
                "referrer": referrer,
                "content": content,
            }
            visitor = Visitor(**data)
            visitor.save()
        if getattr(content, "visitor_count", None) is not None:
            content.visitor_count += 1
            content.save()
        cache.set(cache_key, 1, timeout)
