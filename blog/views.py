from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from articles.models import Article


def home(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(
        request,
        'home.html',
        context
    )


def custom_login(request):
    if request.user.is_authenticated():
        return redirect('admin')

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


def admin(request):
    return render(
        request,
        'admin.html'
    )