from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    # url(r'^proj/', include('proj.foo.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #url(r'^login/$', 'app.views.login_user', name='login_user'),
    url(r'^logout/$', "app.views.logout_user", name='logout_user'),
    url(r'^settings/$', "app.views.settings", name='settings'),
    url(r'^sendEmail/$', "app.views.sendEmail", name='sendEmail'),
    url(r'^jsonRPC/$', "app.views.jsonRPC", name='jsonRPC'),
    url(r'^updateValidTo/$', "app.views.updateValidTo", name='updateValidTo'),
    url(r'^jsonOpenDoor/(?P<user_id>\d+)/?$', "app.views.jsonOpenDoor", name='jsonOpenDoor'),
    url(r'^jsonCloseDoor/(?P<user_id>\d+)/?$', "app.views.jsonCloseDoor", name='jsonCloseDoor'),
    url(r'^jsonCheckIfCanOpen/(?P<user_id>\d+)/?$', "app.views.jsonCheckIfCanOpen", name='jsonCheckIfCanOpen'),
    #url(r'^search_user_in_ldap/$', "app.views.search_user_in_ldap", name='ldap_user'),
    #url(r'^login/$', 'auth.views.login_user', name='login'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)