"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin

urlpatterns = [
    url(r'$', 'articles.views.homepage'),
    url(r'^f1m2', 'articles.views.Feature1_Module2'),
    url(r'^f1m1', 'articles.views.Feature1_Module1'),
    url(r'^f2', 'articles.views.Feature2'),
    url(r'^f4', 'articles.views.index'),
   
    #url(r'^admin/', admin.site.urls),
]
