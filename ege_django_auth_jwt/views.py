"""
MIT License

Copyright (c) 2018 IFRN - Campus EaD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import urllib
import jwt
import requests
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.generic import View

"""
http://provider:8001/jwt/authorize
/?client_id=_SUAPSSO_JWT_CLIENT_ID_
&redirect_uri=http%3A%2F%2Fclient%3A8000%2Fjwt%2Fcomplete%2Fjwt%2Fcomplete%2F%3Foriginal_next%3D%252Fdashboard
"""
SUAPSSO_JWT_AUTHENTICATE_PATTERN = '{root_url}jwt/authorize/' \
                                   '?client_id={client_id}' \
                                   '&state={state}' \
                                   '&redirect_uri={redirect_uri}'
SUAPSSO_JWT_VALIDATE_PATTERN = '{root_url}jwt/validate/'


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            transaction_token = '1'
            request.session['transaction_token'] = transaction_token

            original_next = urllib.quote_plus(request.GET.get('next', settings.LOGIN_REDIRECT_URL))

            root_site_path = request.build_absolute_uri(reverse('ege_django_auth_jwt:complete'))
            redirect_uri = urllib.quote_plus('{root_site_path}?original_next={original_next}'.
                                             format(root_site_path=root_site_path,
                                                    transaction_token=transaction_token,
                                                    original_next=original_next))

            return redirect(SUAPSSO_JWT_AUTHENTICATE_PATTERN.format(root_url=settings.SUAPSSO_JWT_ROOT_URL,
                                                                    client_id=settings.SUAPSSO_JWT_CLIENT_ID,
                                                                    state=transaction_token,
                                                                    redirect_uri=redirect_uri))


class CompleteView(View):
    @csrf_exempt
    def get(self, request):
        response = requests.post(SUAPSSO_JWT_VALIDATE_PATTERN.format(root_url=settings.SUAPSSO_JWT_ROOT_URL),
                                 {'client_id': 'settings.SUAPSSO_JWT_CLIENT_ID',
                                  'auth_token': request.GET['auth_token']})
        if response.status_code != 200:
            raise Exception("Authentication erro! Invalid status code {code}. Error: <br />{error}".
                            format(code=response.status_code, error=response.text))
        return HttpResponse("JWT_COMPLETE [%s]" % response.text)
