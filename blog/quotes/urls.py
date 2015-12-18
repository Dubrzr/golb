from django.conf.urls import url

from blog.quotes import views


urlpatterns = [
    url(r'^admin/$', views.admin, name='admin_quotes'),
    url(r'^add/$', views.add, name='add_quote'),
    url(r'^delete/$', views.delete, name='del_quote'),
]
