from random import randint

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

# from pytagcloud import create_html_data, make_tags
# from pytagcloud.lang.counter import get_tag_counts

from articles.models import Article
from blog.decorators import never_ever_cache
from blog.quotes.models import Quote


@never_ever_cache
def home(request):
    quote_count = Quote.objects.count()
    if quote_count < 1:
        quote = None
    else:
        random_index = randint(0, quote_count - 1)
        quote = Quote.objects.all()[random_index]


    context = {
        'articles': Article.objects.all(),
        'quote': quote
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


@never_ever_cache
def word_cloud(request):
    # all_text = [a.contents_text for a in Article.objects.all()]
    # tags = make_tags(get_tag_counts(all_text), maxsize=120, minsize=5)
    # tags = [a for a in tags if a['size'] > 7]
    # html = create_html_data(tags, 'images/cloud_large.png', size=(700, 500), fontname='museo-sans-rounded', rectangular=True)
    # context = {
    #     'word_cloud': html
    # }
    return render(
        request,
        'wordcloud.html',
        # context
    )


@login_required
@never_ever_cache
def account_settings(request):
    return None


@never_ever_cache
def admin(request):
    return render(
        request,
        'admin.html'
    )