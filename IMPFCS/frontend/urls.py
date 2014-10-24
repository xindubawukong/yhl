from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^login/$', views.loginUser, name='login'),
    url(r'^logout/$', views.logoutUser, name='logout'),
    url(r'^completeInfo/$', views.completeInfo, name='completeInfo'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^foyer/$', views.foyer, name='foyer'),
)
