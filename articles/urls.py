from django.conf.urls import url,include, url
from django.contrib import admin

urlpatterns = [
    url(r'^all/', 'articles.views.articles'),
    url(r'^get/(?P<article_id>\d+)', 'articles.views.article'),
    #url(r'^', 'articles.views.hello'),
   
    #url(r'^admin/', admin.site.urls),
]
