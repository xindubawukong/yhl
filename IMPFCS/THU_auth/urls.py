from django.conf.urls import patterns, url
from THU_auth import views


urlpatterns = patterns('',
    url(r'^$', views.auth, name='auth'),
)
