from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _



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
