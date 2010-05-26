
# httplib2-pwreset.py

"""

"""

import urllib
import httplib2

http = httplib2.Http('.cache')

pwreset_url = 'http://192.168.1.107:8080/gsdc/gsdc/default/pwreset_form'

headers = {}
headers['Content-type'] = 'application/x-www-form-urlencoded'
headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

pwreset_form = {}
pwreset_form['randomstring'] = '39e50bd1b7c4f0264bdb179e65efc136'
pwreset_form['userid'] = 'tsmith'
pwreset_form['password'] = 'pass12345'
pwreset_form['password2'] = 'pass12345'
pwreset_form['form.submitted'] = '1'

response, content = http.request(pwreset_url, 'POST', headers=headers, body=urllib.urlencode(pwreset_form))

print content
print '=============================================='
print response
print '=============================================='
