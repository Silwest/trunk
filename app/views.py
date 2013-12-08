import json
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.context_processors import csrf
from django.core.mail import EmailMultiAlternatives
from django.forms.models import modelformset_factory
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext, Context
from django.template.loader import get_template
import pyjsonrpc
from app.models import UserProfile

def add_csrf(request, **kwargs):
    """ Add CSRF and user to dictionary.
    """
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


def check_creation_date():
    """
        Sprawdza czy uzytkownik moze jeszcze korzystac z serwisu.
    """
    users = UserProfile.objects.filter(userCard__validTo__lt=datetime.today())# userzy do wyrzucenia
    for user in users:
        user.userCard.can_login = False
        user.userCard.save()


def updateValidTo(request):
    """
        Sprawdza czy uzytkownik moze jeszcze korzystac z serwisu.
    """
    user = UserProfile.objects.get(user=request.user)
    user.userCard.can_login = True
    user.userCard.validTo += timedelta(days=30)
    user.userCard.save()
    messages.add_message(request, messages.SUCCESS, 'Twoje konto zostalo przedluzone.')
    return redirect(home)


def sendEmail(request):
    """
        Funkcja wysylajaca maile do uzytkownikow.
    """
    userProfiles = UserProfile.objects.filter(userCard__can_login=False)
    subject = 'Twoje konto jest nieaktywne!'
    from_email = 'silwestpl@gmail.com'
    template = get_template('email_template.html')
    template_html = template.render(Context({}))
    to = []
    for user in userProfiles:
        to.append(user.user.email)
    msg = EmailMultiAlternatives(subject, '', from_email, to)
    msg.attach_alternative(template_html, "text/html")
    msg.send()
    messages.add_message(request, messages.SUCCESS, 'Mail zostal wyslany do nie aktywnych uzytkownikow!')
    return redirect(home)


@login_required()
def jsonRPC(request):
    http_client = pyjsonrpc.HttpClient(
        url="http://localhost:8080",
        username='Silwest',
        password='test'
    )
    #user = User.objects.get(id=4)
    #p#rint user
    print http_client.call("add", 1, 2)
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    print http_client.add(1, 4)
    today = datetime.today()
    add_days = timedelta(days=30)
    http_client.addDays(json.dumps(datetime.today(), default=dthandler))
    #print http_client.userInfo(user.first_name, user.last_name)@login_required()


def jsonCheckIfCanOpen(request, user_id):
    http_client = pyjsonrpc.HttpClient(
        url="http://localhost:8080",
        username='Silwest',
        password='test'
    )
    userProfile = UserProfile.objects.get(user_id=user_id)
    response = http_client.check(user_id)
    if response:
        messages.add_message(request, messages.SUCCESS, str(userProfile) + ' moze otworzyc drzwi do serwerowni.')
    else:
        messages.add_message(request, messages.WARNING, str(userProfile) + ' nie moze otworzyc drzwi do serwerowni.')

    return HttpResponse(response)

def jsonOpenDoor(request, user_id):
    http_client = pyjsonrpc.HttpClient(
        url="http://localhost:8080",
        username='Silwest',
        password='test'
    )

    response = http_client.openDoor(user_id)
    userProfile = UserProfile.objects.get(user_id=user_id)
    if response:
        messages.add_message(request, messages.SUCCESS, 'Drzwi zostaly zamkniete dla' + str(userProfile))
    else:
        messages.add_message(request, messages.WARNING, 'Blad przy otwieraniu drzwi dla usera.')
    return redirect(home)


def jsonCloseDoor(request, user_id):
    http_client = pyjsonrpc.HttpClient(
        url="http://localhost:8080",
        username='Silwest',
        password='test'
    )

    response = http_client.closeDoor(user_id)
    userProfile = UserProfile.objects.get(user_id=user_id)
    if response:
        messages.add_message(request, messages.SUCCESS, 'Drzwi zostaly otworzone dla' + str(userProfile))
    else:
        messages.add_message(request, messages.WARNING, 'Blad przy otwieraniu drzwi dla usera.')
    return redirect(home)
    #with open('doors.txt', 'r') as file:
    #    data = file.readlines()
    #for (counter, line) in enumerate(data):
    #    if line[0] == user_id:
    #        data[counter] = str(user_id + ' 1\n')
    #with open('doors.txt', 'w') as file:
    #    file.writelines(data)





    #
    ##user = User.objects.get(id=4)
    ##p#rint user
    #print http_client.call("add", 1, 2)
    #dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    #print http_client.add(1, 4)
    #today = datetime.today()
    #add_days = timedelta(days=30)
    #http_client.addDays(json.dumps(datetime.today(), default=dthandler))
    ##print http_client.userInfo(user.first_name, user.last_name)


@login_required()
def home(request):
    users = UserProfile.objects.all()
    check_creation_date()
    logged_user = UserProfile.objects.get(user=request.user)
    return render_to_response('home.html', add_csrf(request,
                                                    users=users,
                                                    logged_user=logged_user,
                                            ), context_instance=RequestContext(request))


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

#
#@login_required()
#def search_user_in_ldap(request, search=None):
#    ldap_obj = LDAPBackend()
#    #user = ldap_obj.populate_user('0tomasze')
#    search_filter = "(|(sn=*"+ search + " *)(displayName=*" + search + "*))"
#    search_scope = ldap.SCOPE_SUBTREE
#    retrive_attributes = ["displayName", "mail"]
#    try:
#        ldap_result_id = ldap_obj.search('', search_scope, search_filter, retrive_attributes)
#        while 1:
#            _, user = l.result
#    #LDAPSearch("o=fis", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
#    print user.is_anonymous()
