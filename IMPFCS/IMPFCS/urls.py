from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IMPFCS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^site/', include('frontend.urls', namespace='frontend')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/$', include('THU_auth.urls', namespace='THU_auth')),
)
