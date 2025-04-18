import re
from django.conf import settings
from django.shortcuts import redirect

# Compile je exempt‑URL’s (regex‑patronen) uit settings
EXEMPT_URLS = []
# Zorg dat LOGIN_URL zelf nooit beschermd wordt
if settings.LOGIN_URL:
    EXEMPT_URLS.append(re.compile(settings.LOGIN_URL.lstrip('/')))
# Voeg je eigen exempt‑patronen toe uit settings
for expr in getattr(settings, 'LOGIN_EXEMPT_URLS', []):
    EXEMPT_URLS.append(re.compile(expr))

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')  # bv. 'planning/planboard/'
        # Als gebruiker niet ingelogd én path komt niet in EXEMPT_URLS:
        if not request.user.is_authenticated:
            if not any(pattern.match(path) for pattern in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
        # Anders gewoon door naar de view
        return self.get_response(request)
