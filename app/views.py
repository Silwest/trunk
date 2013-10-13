# Create your views here.
# Create your views here.
from atom.http_core import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext




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
    #logout(request)
    print 'Iam here'
    username = password = ''
    if request.POST:
        print 'HEre'
        username = request.POST.get('username')
        password = request.POST.get('password')
        print request.POST
        print username
        print password
        user = authenticate(username=username, password=password)
        print 'and here'
        print user
        print user is None
        if user is not None:
            if user.is_active:
                print user
                login(request, user)
                print 'eherees'
                return HttpResponseRedirect('/')
    #return render_to_response('login.html', context_instance=RequestContext(request))
    return render_to_response('login.html', add_csrf(request,
                                                     ), context_instance=RequestContext(request))


@login_required()
def main(request):
    pass