from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add),
    url(r'^books/login$', views.login),
    url(r'^books/register$', views.register),
    url(r'^books/logout$', views.logout),
    url(r'^books/add_br$', views.add_br),
    url(r'^books/add_r$', views.add_r),
    url(r'^books/delete_r/(?P<id>\d+)/(?P<id2>\d+)$', views.delete_r),
    url(r'^books/(?P<id>\d+)$', views.review),
    url(r'^books/users/(?P<id>\d+)$', views.user),
  ]
