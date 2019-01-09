from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect


class EgeAdminSite(AdminSite):

    @never_cache
    def login(self, request, extra_context=None):
        return redirect(settings.LOGIN_URL)
        # print("EgeAdminSite.login(request=%s, extra_context=%s)" % (request, extra_context))
        # return super(EgeAdminSite, self).login(request, extra_context)


ege_admin_site = EgeAdminSite(name='ege_admin_site')
