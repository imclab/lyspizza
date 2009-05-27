from django.conf.urls.defaults import *
from lyspizza.main.views import *
import django.contrib.auth.views
urlpatterns = patterns('main',
                       (r'^accounts/login/$', django.contrib.auth.views.login, {'template_name': 'login.html',
                                                                       'redirect_field_name': 'next'}),
                       (r'^accounts/logout/$', django.contrib.auth.views.logout, {'next_page': '/'}),
                       (r'^accounts/register/$', register),
                       (r'^$', index),
                       (r'^occasion/(?P<occasion_id>\d+)/$', occasion_view),
                       )
