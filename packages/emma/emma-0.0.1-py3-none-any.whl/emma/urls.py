"""emma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from . import views

admin.site.index_title = 'Emma'
admin.site.site_header = 'Emma'
admin.site.site_title = 'Emma'

urlpatterns = [
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    path('emma/browse/', views.browse, name='browse'),
    path('emma/browse/<time>/', views.browse, name='browse-time'),
    path('emma/browse/<time>/next/', views.browse_next, name='browse-next'),
    path('emma/browse/<time>/prev/', views.browse_prev, name='browse-prev'),
    path('emma/histogram/', views.histogram, name='histogram'),
    path('', admin.site.urls),
]
