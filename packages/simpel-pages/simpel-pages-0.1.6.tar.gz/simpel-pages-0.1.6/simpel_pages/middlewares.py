from django.conf import settings
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin

from .views import simpelpage


class SimpelPageMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response  # No need to check for a simpelpage for non-404 responses.
        try:
            return simpelpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
