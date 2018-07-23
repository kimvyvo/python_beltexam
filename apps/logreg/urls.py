from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^quotes', views.quotes),
    url(r'^myaccount/(?P<id>\d+)', views.edit),
    url(r'^update/(?P<id>\d+)', views.update),
    url(r'^user/(?P<id>\d+)', views.display),
    url(r'^like', views.like),
    url(r'^add_quote', views.add_quote),
    url(r'^delete', views.delete),
    url(r'^logout$', views.logout),
]