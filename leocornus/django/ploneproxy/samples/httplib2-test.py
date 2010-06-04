
# httplib2-test.py

"""
a small script try to use httplib2 to do backend login to a Plone site through
the login_form.

this dpends on the httplib2 module: http://code.google.com/p/httplib2/
"""

import urllib
from Cookie import SimpleCookie

import httplib2

http = httplib2.Http('.cache')

login_url = 'http://internal.host.name/Plone/login_form'

headers = {}
headers['Content-type'] = 'application/x-www-form-urlencoded'
headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers['Leocornus-Header'] = 'Leocornus Django PloneProxy (httplib2)'

login_form = {}
login_form['__ac_name'] = 'username'
login_form['__ac_password'] = 'password'
login_form['cookies_enabled'] = '1'
login_form['js_enabled'] = '0'
login_form['form.submitted'] = '1'

response, content = http.request(login_url, 'POST', headers=headers, body=urllib.urlencode(login_form))

print content
print '=============================================='
print response
print '=============================================='

cookie = SimpleCookie()
cookie.load(response['set-cookie'])

for key in cookie.keys():
    print key
    print '===================='
    print cookie.get(key).value
    print '=============================================='
