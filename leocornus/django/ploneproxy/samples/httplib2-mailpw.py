
# httplib2-mainpw.py

"""

"""

import urllib
import httplib2

http = httplib2.Http('.cache')

mailpw_url = 'http://10.20.9.65:8080/gsdc/gsdc/default/mail_password'

headers = {}
headers['Content-type'] = 'application/x-www-form-urlencoded'
headers['User-Agent'] = 'Leocornus Django PloneProxy'

mail_form = {}
mail_form['userid'] = 'tsmith'

response, content = http.request(mailpw_url, 'POST', headers=headers, body=urllib.urlencode(mail_form))

print content
print '=============================================='
print response
print '=============================================='
