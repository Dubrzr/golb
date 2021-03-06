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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.views import logout

from articles.urls import urlpatterns as articles_urlpatterns
from blog import settings, views
from blog.quotes import urls as quote_urlpatterns
from users.urls import urlpatterns as users_urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.custom_login, name='login'),
    url(r'^account/$', views.account_settings, name='account_settings'),
    url(r'^logout/$', logout, {'next_page': 'blog.views.home'}, name='logout'),
    url(r'^word_cloud/$', views.word_cloud, name='word_cloud'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'article/', include(articles_urlpatterns)),
    url(r'user/', include(users_urlpatterns)),
    url(r'quote/', include(quote_urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
