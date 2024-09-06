# middleware.py

from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # AuthenticationMiddleware が正しく処理されていることを確認
        if not hasattr(request, 'user'):
            # AuthenticationMiddleware が適用されていない場合
            return self.get_response(request)
        
        if not request.user.is_authenticated and request.path not in [settings.LOGIN_URL, settings.LOGOUT_URL, settings.SIGNUP_URL]:
            return redirect(settings.LOGIN_URL)
        
        response = self.get_response(request)
        return response
