from django.contrib import admin
from django.urls import path


# صفحه‌های اصلی سایت در فاز دوم اضافه می‌شوند.
urlpatterns = [
    path("admin/", admin.site.urls),
]
