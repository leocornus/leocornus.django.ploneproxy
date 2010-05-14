
# models.py

"""
models for Django Plone Proxy.
"""

from django.db.models import Model
from django.db.models import Manager
from django.db.models import IntegerField
from django.db.models import CharField
from django.db.models import TextField

from django.utils.translation import ugettext_lazy as _

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

#class PloneAuthenStateManager(Manager):
#    """
#    """
#
#    def create_state(self, )

class PloneAuthenState(Model):
    """

    # trying the doctest
    >>> state = PloneAuthenState(user_id=1, status='valid',
    ... cookie_name='__ac', cookie_value='value')
    >>> state.save()

    # we should find it now.
    >>> theOne = PloneAuthenState.objects.get(user_id=1)
    >>> theOne.cookie_value
    u'value'
    """

    user_id = IntegerField(_('User Id'), primary_key=True)
    status = CharField(_('Authentication Status'), max_length=8)
    cookie_name = CharField(_('Cookie Name'), max_length=60)
    cookie_value = TextField(_('Cookie Value'))

    #objects = PloneAuthenStateManager()
