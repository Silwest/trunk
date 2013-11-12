from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from app.models import UserProfile
from django.core.mail import EmailMultiAlternatives

def add_csrf(request, **kwargs):
    """ Add CSRF and user to dictionary.
    """
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


def sendEmail(request):
    """
        Funkcja wysylajaca maile do uzytkownikow.
    """
    subject, from_email, to = 'hello', 'silwestpol@gmail.com', 'silwestpol@gmail.com'
    text_content = 'This is important'
    html_content = '<p>cos</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@login_required()
def home(request):
    print request.user
    return render_to_response('home.html', add_csrf(request), context_instance=RequestContext(request))


def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Logged in.')
                return HttpResponseRedirect('/')
    return render_to_response('login.html', add_csrf(request,
                                                     ), context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out.')
    return redirect_to_login(next='')


@login_required()
def main(request):
    pass


@login_required()
def settings(request):
    user_profile = UserProfile.objects.filter(user=request.user)
    user_profile_form = modelformset_factory(UserProfile, extra=0)
    if request.method == 'POST':
        formset = user_profile_form(request.POST)
        if formset.is_valid:
            formset.save()
    formset = user_profile_form(queryset=user_profile)

    return render_to_response('settings.html', add_csrf(request,
                                                       user_profile=user_profile[0],
                                                       formset=formset,
                                                       ), context_instance=RequestContext(request))
