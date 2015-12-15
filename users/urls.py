from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^$', views.list_all, name='users'),
    url(r'^admin/$', views.admin, name='admin_users'),
    url(r'^add/$', views.add, name='add_user'),
    url(r'^delete/$', views.delete, name='del_user'),
]
