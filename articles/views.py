from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from articles.models import Article, History
from blog.decorators import never_ever_cache


@never_ever_cache
def list_all(request):
    articles = Article.objects.filter(state='PU').order_by('-created_at')
    years = list(set([a.created_at.year for a in articles]))

    class Year():
        def __init__(self, year, articles):
            self.year = year
            self.articles = articles

    result_years = []
    for year in years:
        articles = articles.filter(created_at__year=year)
        result_years.append(Year(year, articles))

    context = {
        'years': result_years
    }
    return render(
        request,
        'article/articles.html',
        context
    )


@login_required
@never_ever_cache
def admin(request, error=None):
    context = {
        'articles': Article.objects.all(),
        'error': error,
        'languages': Article.LANGUAGES_CHOICES
    }
    return render(
        request,
        'article/admin.html',
        context
    )


@login_required
@never_ever_cache
def add(request):
    error = None
    if request.POST:
        article_data = {
            'title': request.POST.get('title'),
            'language': request.POST.get('language')
        }
        if None in [k for v, k in article_data.items()]:
            error = 'Veuillez remplir tous les champs.'
        else:
            try:
                article = Article.objects.create(**article_data)
                article.authors.add(request.user)
                article.save()
            except Exception as e:
                error = 'Champs invalides. ({})'.format(e)

    if error:
        return admin(request, error)
    return admin(request)


@login_required
@never_ever_cache
def edit(request, id, history_id=None):
    article = get_object_or_404(Article, id=id)
    if request.POST:
        article_data = {
            'title': request.POST.get('title'),
            'contents': request.POST.get('contents')
        }
        if None in [k for v, k in article_data.items()]:
            raise Http404()
        else:
            article.title = article_data['title']
            article.update_contents(request.user, article_data['contents'])
            article.save()
    if history_id is None:
        history = article.history
    else:
        history = get_object_or_404(History, id=history_id)
    context = {
        'article': article,
        'contents': history.get_contents() if history else ""
    }
    return render(
        request,
        'article/editor.html',
        context
    )


@login_required
@never_ever_cache
def delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.state = 'RE'
    article.save()


@login_required
@never_ever_cache
def history(request, id):
    article = get_object_or_404(Article, id=id)
    history = []
    h = article.history
    while h:
        history.append(h)
        h = h.parent
    context = {
        'article': article,
        'history': history
    }
    return render(
        request,
        'article/history.html',
        context
    )


@never_ever_cache
def article(request, id):
    article = get_object_or_404(Article, id=id)
    if article.state != 'PU':
        raise Http404()

    context = {
        'article': article
    }
    return render(
        request,
        'article/article.html',
        context
    )


@login_required
@never_ever_cache
def update_state(request, id, state):
    article = get_object_or_404(Article, id=id)
    try:
        article.update_state(state)
    except ValueError:
        raise Http404()
    return edit(request, id=id)
