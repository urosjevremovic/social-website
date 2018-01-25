from django.http import HttpResponseBadRequest
from functools import wraps


def ajax_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('<h1>Bad Request (400)</h1>', content_type='text/html')
        return f(request, *args, **kwargs)
    return wrap
