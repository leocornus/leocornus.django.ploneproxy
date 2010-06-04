
# admin.py

"""
registering models to Django default admin interface.
"""

from django.contrib import admin
from django.contrib.sessions.models import Session

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class SessionAdmin(admin.ModelAdmin):
    """
    admin class for Session model
    """

    list_display = ('expire_date', 'session_key')
    list_filter = ('expire_date',)
    ordering = ('expire_date',)

admin.site.register(Session, SessionAdmin)
