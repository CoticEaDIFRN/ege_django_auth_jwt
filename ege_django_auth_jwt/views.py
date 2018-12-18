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
import jwt
import requests
from urllib.parse import quote_plus
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.generic import View

"""
http://provider:8001/jwt/authorize
/?client_id=_EGE_JWT_CLIENT_ID_
&redirect_uri=http%3A%2F%2Fclient%3A8000%2Fjwt%2Fcomplete%2Fjwt%2Fcomplete%2F%3Foriginal_next%3D%252Fdashboard
"""
EGE_VALIDATE_JWT_VALIDATE_PATTERN = ''


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            transaction_token = '1'
            request.session['transaction_token'] = transaction_token

            original_next = quote_plus(request.GET.get('next', settings.LOGIN_REDIRECT_URL))

            root_site_path = request.build_absolute_uri(reverse('ege_django_auth_jwt:complete'))
            redirect_uri = quote_plus('%s?original_next=%s' % (root_site_path, original_next))

            return redirect('%s?client_id=%s&state=%s&redirect_uri=%s' %
                            (settings.EGE_ACESSO_JWT_AUTHORIZE,
                             settings.EGE_ACESSO_JWT_CLIENT_ID,
                             transaction_token,
                             redirect_uri))


class CompleteView(View):
    @csrf_exempt
    def get(self, request):
        print('%s?client_id=%s&auth_token=%s' %
                                 (settings.EGE_ACESSO_JWT_VALIDATE,
                                  settings.EGE_ACESSO_JWT_CLIENT_ID,
                                  request.GET['auth_token']))
        response = requests.get('%s?client_id=%s&auth_token=%s' %
                                (settings.EGE_ACESSO_JWT_VALIDATE,
                                 settings.EGE_ACESSO_JWT_CLIENT_ID,
                                 request.GET['auth_token']))
        if response.status_code != 200:
            raise Exception("Authentication erro! Invalid status code %s. Error: <br />%s" %
                            (response.status_code, response.text))
        return HttpResponse("JWT_COMPLETE [%s]" % response.text)
"""
EGE_ACESSO_URL=http://acesso/id/acesso/
EGE_ACESSO_JWT_AUTHORIZE=http://localhost/id/acesso/jwt/authorize/
EGE_ACESSO_JWT_VALIDATE=http://localhost/id/acesso/jwt/validate/
EGE_ACESSO_JWT_CLIENT_ID=_EGE_ACESSO_JWT_CLIENT_ID_
"""