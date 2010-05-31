from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^first/', include('first.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #(r'^polls/$', 'first.hello.views.index'),
    #(r'^login/$', 'first.hello.views.login'),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'leocornus.django.ploneproxy.views.login'),
    (r'^mail_password/$', 'leocornus.django.ploneproxy.views.mailPassword'),
    (r'^password_reset/$', 'leocornus.django.ploneproxy.views.passwordReset'),
    (r'^logout/$', 'leocornus.django.ploneproxy.views.logout')
)
