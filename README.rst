|pypi-version|_ |pypi-download|_ |pypi-license|_ 

leocornus.django.ploneproxy
===========================

A Django application as a Proxy to Plone sites.

Overview
--------

Leocornus django ploneproxy is trying to provide a mod_python
PythonAuthenHandler implementation and a Django application, which
will allow Plone user can access internal Plone site through a 
http proxy server.

The http proxy server will authenicate user credentials based on 
backend Plone user sources and provide a extra session on top of
Plone's session (cookie).

The Django application provides the login form and manages the 
active session on proxy server layer.

.. |pypi-version| image:: http://img.shields.io/pypi/v/leocornus.django.ploneproxy.svg
.. _pypi-version: https://pypi.python.org/pypi/leocornus.django.ploneproxy
.. |pypi-download| image:: http://img.shields.io/pypi/dm/leocornus.django.ploneproxy.svg
.. _pypi-download: https://pypi.python.org/pypi/leocornus.django.ploneproxy
.. |pypi-license| image:: http://img.shields.io/pypi/l/leocornus.django.ploneproxy.svg
.. _pypi-license: https://pypi.python.org/pypi/leocornus.django.ploneproxy
