"""bookEx URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# import the Register view from your app
from bookMng.views import Register
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bookMng.urls")),
    path("", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path("admin/", admin.site.urls),

    # your app’s pages
    path("", include("bookMng.urls")),

    # registration flow
    path("register", Register.as_view(), name="register"),
    path(
        "register/success",
        TemplateView.as_view(template_name="registration/register_success.html"),
        name="register-success",
    ),

    # built-in auth views: /login, /logout, /password_change, etc.
    path("", include("django.contrib.auth.urls")),
]
