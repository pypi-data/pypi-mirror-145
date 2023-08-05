try:
    from django.urls import re_path
except ImportError:  # Django 1.11
    from django.conf.urls import url as re_path
from django.contrib import admin

from testapp.models import Product


admin_site = admin.AdminSite()
admin_site.register(Product)

urlpatterns = [
    re_path(r'^admin/', admin_site.urls),
]
