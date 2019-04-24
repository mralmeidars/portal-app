"""portal URL Configuration

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
from django.urls import include, path
from django.contrib import admin
from portal.app import views

admin.autodiscover()

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('portal/', views.loadPortal, name='portal'),
    path('portal/twitterlists', views.loadDashboardTwitter, {'_typeReport':'lists'}, name='twitterlists'),
    path('portal/twittergraphs', views.loadDashboardTwitter, {'_typeReport':'graphs'}, name='twittergraphs'),
    path('portal/googlelists', views.loadDashboardGoogle, {'_typeReport':'lists'}, name='googlelists'),
    path('portal/googlegraphs', views.loadDashboardGoogle, {'_typeReport':'graphs'}, name='googlegraphs'),
    path('admin/', admin.site.urls),
]
