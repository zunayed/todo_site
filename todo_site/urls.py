from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api_v1/', include('todo_app.urls', namespace='api_v1')),
    url(r'^admin/', include(admin.site.urls)),
)
