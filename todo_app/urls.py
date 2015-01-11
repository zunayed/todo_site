from django.conf.urls import patterns, url

from todo_app import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^todos/$', views.todos, name='todos'),
    url(r'^todos/(?P<id>.+)$', views.get_todo, name='get_todo'),

)
