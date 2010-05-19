
# views.py

"""
django view classes for leocornus.django.ploneproxy
"""

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def login(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    accept = request.POST.get('accept_disclaimer', '')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            from django.contrib.auth import login
            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    # decide another available language.
    lang = get_language()
    uri =  request.build_absolute_uri()
    lang_name, lang_link = prepareOtherLang(request.REQUEST, lang, uri)

    import pdb; pdb.set_trace()
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'lang_name' : lang_name,
        'lang_link' : lang_link,
    }, context_instance=RequestContext(request))

login = never_cache(login)


def prepareOtherLang(req, currentLang, uri):

    if currentLang == 'en':
        lang_code = 'fr'
        lang_name = u'Francais'
    else:
        lang_code = 'en'
        lang_name = 'English'

    # get the language parameter name.
    try:
        paramName = settings.PLONEPROXY_LANG_PARAM_NAME
        if not paramName:
            # set to None, then we use default.
            paramName = 'ldp_lang'
    except AttributeError:
        # using the default Plone cookie name.
        paramName = 'ldp_lang'
    langs = req.getlist(paramName)

    if len(langs) > 0:
        # the current parameters.
        current = ''
        for lang in langs:
            one = '%s=%s' % (paramName, lang)
            if (langs.index(lang) + 1) < len(langs):
                one = one + '&'
            current = current + one
        # the new param
        newStr = '%s=%s' % (paramName, lang_code)
        # replace!
        lang_link = uri.replace(current, newStr)
    else:
        if uri.find(u'?') > 0:
            lang_link = '%s&%s=%s' % (uri, paramName, lang_code)
        else:
            lang_link = '%s?%s=%s' % (uri, paramName, lang_code)

    return (lang_name, lang_link)
