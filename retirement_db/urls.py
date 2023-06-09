"""retirement_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from form5500.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('viz',charts, name='charts'),
    path('map',map, name='map'),
    path('',search_state, name='state'),
    path('industry',search_industry, name='industry'),
    path('asset',search_asset, name='asset'),
    path('state_export/<q>',state_export,name='state_export'),
    path('industry_export/<q>',industry_export,name='industry_export'),
    path('asset_export/<q>',asset_export,name='asset_export')
]
