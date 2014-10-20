from django.conf.urls import patterns, url
from users import views


urlpatterns = patterns('',
    url(r'^test/$', views.test, name='test'),
    url(r'^addUser/$', views.addUser, name='addUser'),
    url(r'^removeUser/$', views.removeUser, name='removeUser'),
    url(r'^userLogin/$', views.userLogin, name='userLogin'),
    url(r'^userLogout/$', views.userLogout, name='userLogout'),
)
