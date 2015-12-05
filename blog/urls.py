"""site URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import logout

import blog.views as blog_views
from blog import settings

urlpatterns = [
    url(r'^$', blog_views.home, name='home'),
    url(r'^login/$', blog_views.custom_login, name='login'),
    url(r'^account/$', blog_views.account_settings, name='account_settings'),
    url(r'^logout/$', logout, {'next_page': 'blog.views.home'}, name='logout'),
    url(r'^admin/$', blog_views.admin, name='admin'),
    url(r'^admin/add_user/$', blog_views.add_user, name='add_user'),
    url(r'^admin/del_user/$', blog_views.del_user, name='del_user'),
    url(r'^editor/$', blog_views.editor, name='editor'),
    url(r'^word_cloud/$', blog_views.word_cloud, name='word_cloud'),
    url(r'^all_articles/$', blog_views.all_articles, name='all_articles'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
