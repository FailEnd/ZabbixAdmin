# ~*~ coding: utf-8 ~*~
from django.http import HttpResponseRedirect


class LoginMiddleware:
    SAFE_URL_PATTERN = ('/login/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session._session:
            response = self.get_response(request)
            return response
        else:
            if request.path == self.SAFE_URL_PATTERN:
                response = self.get_response(request)
                return response
            else:
                return HttpResponseRedirect("/login/")