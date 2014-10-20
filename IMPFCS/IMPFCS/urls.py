from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IMPFCS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/users/', include('users.urls', namespace='users')),
    url(r'^admin/', include(admin.site.urls)),
)
