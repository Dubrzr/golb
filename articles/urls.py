from django.conf.urls import url

from articles import views

urlpatterns = [
    url(r'^$', views.list_all, name='articles'),
    url(r'^(?P<id>[0-9]+)/$', views.article, name='article'),
    url(r'^admin/$', views.admin, name='admin_articles'),
    url(r'^add/$', views.add, name='add_article'),
    url(r'^delete/$', views.delete, name='del_article'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name='edit_article'),
    url(r'^edit/(?P<id>[0-9]+)/(?P<history_id>[0-9]+)/$', views.edit, name='edit_article'),
    url(r'^history/(?P<id>[0-9]+)/$', views.history, name='history_article'),
    url(r'^update_state/(?P<id>[0-9]+)/(?P<state>[A-Z]+)/$', views.update_state, name='update_state_article'),
]
