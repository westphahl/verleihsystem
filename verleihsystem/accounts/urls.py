from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^profile/$', 'accounts.views.change_user_profile',
        name='user_profile_form'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
