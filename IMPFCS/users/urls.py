from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
  url(r'^manage/apply/list$', views.listApplications, name='listApplications'),
  url(r'^manage/teamMember/accept$', views.teamMemberAccept, name='teamMemberAccept'),
  url(r'^manage/teamMember/reject$', views.teamMemberReject, name='teamMemberReject'),
)
