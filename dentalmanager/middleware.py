# dentalmanager/middleware.py

import re
from django.conf import settings
from django.shortcuts import redirect

EXEMPT_URLS = [
    re.compile(settings.LOGIN_URL.lstrip('/')),
]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated:
            if not any(p.match(path) for p in EXEMPT_URLS):
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return self.get_response(request)
