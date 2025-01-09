from django.contrib import admin 
from django.urls import include, path 

urlpatterns = [
    path("", include("game.urls")),
    path("admin/", admin.site.urls),
    path("accounts/",include("django.contrib.auth.urls")),
]
