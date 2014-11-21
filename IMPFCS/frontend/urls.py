from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^login/$', views.loginUser, name='login'),
    url(r'^logout/$', views.logoutUser, name='logout'),
    url(r'^completeInfo/$', views.completeInfo, name='completeInfo'),
    url(r'^foyer/$', views.foyer, name='foyer'),
    url(r'^message/$', views.message, name='message'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^scores/$', views.scores, name='scores'),
    url(r'^competitions/$', views.competitions, name='competitions'),
    url(r'^applyTeam/$', views.applyTeam, name='applyTeam'),
    url(r'^profile/$', views.profile, name='profile'),
    #url(r'^userManagement/$', views.userManagement, name='userManagement'),
    #url(r'^resourceManagement/$', views.resourceManagement, name='resourceManagement'),
    url(r'^management/$', views.management, name='management'),
    url(r'^addResource/$', views.addResource, name='addResource'),
    url(r'^applyResource/(?P<resource_id>[a-z0-9]+)/$', views.applyResource, name='applyResource'),
    url(r'^replyResourceApplication/(?P<reply>[a-z]+)/(?P<application_id>[a-z0-9]+)/$', views.replyResourceApplication, name='replyResourceApplication'),
    url(r'^replyTeamApplication/(?P<reply>[a-z]+)/(?P<application_id>[a-z0-9]+)/$', views.replyTeamApplication, name='replyTeamApplication'),
)
