from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from blog.models import User, UserManager
from posts.models import Article


def home(request):
    return render(
        request,
        'home.html'
    )


def custom_login(request):
    if request.user.is_authenticated():
        raise Http404()

    error = None
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        stay_connected = request.POST.get('stay_connected', False)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if stay_connected:
                # Session will expires in 30 days
                request.session.set_expiry(30*86400)
            return HttpResponseRedirect(reverse('blog.views.home'))
        else:
            error = _("Nom d'utilisateur ou mot de passe incorrect.")
    context = {
        'error': error
    }
    return render_to_response(
        'login.html',
        context,
        context_instance=RequestContext(request)
    )

def word_cloud(request):
    return None

@login_required
def account_settings(request):
    return None

@login_required
def admin(request, error=None):
    if not request.user.is_admin:
        raise Http404()

    context = {
        'users': User.objects.all(),
        'error': error
    }
    return render(
        request,
        'admin.html',
        context
    )

@login_required
def add_user(request):
    if not request.user.is_admin:
        raise Http404()

    error = None
    if request.POST:
        user_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'password': request.POST.get('password'),
        }
        if None in [k for v, k in user_data.items()]:
            error = 'Veuillez remplir tous les champs.'
        else:
            try:
                if int(request.POST.get('type')): # Is admin
                    User.objects.create_superuser(**user_data)
                else:
                    User.objects.create_user(**user_data)
            except Exception as e:
                error = 'Champs invalides. ({})'.format(e)

    if error:
        return admin(request, error)
    return redirect('admin', error=error)

@login_required
def del_user(request):
    if not request.user.is_admin:
        raise Http404()

    if request.GET:
        user_id = request.GET.get('user_id')
        try:
            u = User.objects.get(id=user_id)
        except:
            raise Http404()
        if u == request.user:
            raise Http404()
        u.delete()

    return redirect('admin')


def all_articles(request):
    return None

@login_required
def editor(request, error=None):
    context = {
        'articles': Article.objects.all(),
        'error': error
    }
    return render(
        request,
        'editor.html',
        context
    )