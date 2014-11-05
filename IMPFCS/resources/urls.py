from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^manage/add/$', views.addResource, name='addResource'),
    url(r'^manage/cancel/$', views.cancelResource, name='cancelResource'),
    url(r'^manage/cancelone/$', views.cancelResourceOne,
        name='cancelResourceOne'),
    url(r'^manage/apply/list$', views.listApplies, name='listApplies'),
    url(r'^manage/apply/reply$', views.replyApply, name='replyApply'),
    url(r'^list/$', views.listResources, name='listResources'),
    url(r'^view/$', views.viewResource, name='viewResource'),
    url(r'^apply/$', views.applyResource, name='applyResource'),
    url(r'^apply/list$', views.listMyApplies, name='listMyApplies'),
)
