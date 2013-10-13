from atom.http_core import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from app.models import UserProfile


def add_csrf(request, **kwargs):
    """ Add CSRF and user to dictionary.
    """
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


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
        print user is None
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('login.html', add_csrf(request,
                                                     ), context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return redirect_to_login(next='')




@login_required()
def main(request):
    pass

@login_required()
def settings(request):
    user_profile = UserProfile.objects.filter(user=request.user)
    user_profile_form = modelformset_factory(UserProfile, extra=0)
    formset = user_profile_form(queryset=user_profile)

    return render_to_response('settings.html',add_csrf(request,
                                                       user_profile=user_profile,
                                                       formset=formset,
                                                       ), context_instance=RequestContext(request))