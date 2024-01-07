from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

class AdminSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            admin_cookie = request.COOKIES.get('adminsessionid')
            if admin_cookie:
                request.COOKIES[settings.SESSION_COOKIE_NAME] = admin_cookie
        super().process_request(request)

    def process_response(self, request, response):
        if request.path.startswith('/admin/'):
            # Встановлюємо адміністративну сесійну cookie
            if response.cookies.get(settings.SESSION_COOKIE_NAME):
                cookie = response.cookies[settings.SESSION_COOKIE_NAME]
                response.set_cookie(
                    'adminsessionid',
                    cookie.value,
                    max_age=cookie['max-age'],
                    expires=cookie['expires'],
                    path=cookie['path'],
                    domain=cookie['domain'],
                    secure=cookie['secure'],
                    httponly=cookie['httponly'],
                    samesite=cookie['samesite']
                )
                # Видаляємо звичайну сесійну cookie
                response.delete_cookie(settings.SESSION_COOKIE_NAME)
        return super().process_response(request, response)
