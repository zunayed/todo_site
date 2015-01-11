from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api_v1/', include('todo_app.urls', namespace='api_v1')),
    url(r'^admin/', include(admin.site.urls)),
)
