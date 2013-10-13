from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    # url(r'^proj/', include('proj.foo.urls')),
    url(r'^login/$', 'app.views.login_user', name='login_user'),
    url(r'^logout/$', "app.views.logout_user", name='logout_user'),
    url(r'^settings/$', "app.views.settings", name='settings'),
    #url(r'^login/$', 'auth.views.login_user', name='login'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)