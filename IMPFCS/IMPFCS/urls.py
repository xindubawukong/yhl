from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


urlpatterns = [
    # Examples:
    # url(r'^$', 'IMPFCS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', lambda request: HttpResponseRedirect(reverse('frontend:foyer'))),
    url(r'^site/', include('frontend.urls', namespace='frontend')),
#    url(r'^ccc/',views.ccc),
]