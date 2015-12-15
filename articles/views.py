from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache, cache_control
from articles.models import Article, History


def list_all(request):
    articles = Article.objects.all()
    years = list(set([a.created_at.year for a in articles]))

    class Year():
        def __init__(self, year, articles):
            self.year = year
            self.articles = articles

    result_years = []
    for year in years:
        articles = Article.objects.filter(created_at__year=year)
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
def add(request):
    error = None
    if request.POST:
        article_data = {
            'title': request.POST.get('title'),
            'language': request.POST.get('language'),
        }
        if None in [k for v, k in article_data.items()]:
            error = 'Veuillez remplir tous les champs.'
        else:
            try:
                article = Article.objects.create(**article_data)
                article.authors.add(request.user)

            except Exception as e:
                error = 'Champs invalides. ({})'.format(e)

    if error:
        return admin(request, error)
    return redirect('admin_articles')


@login_required
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
def delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.state = 'RE'
    article.save()


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
@login_required
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


def article(request, id):
    article = get_object_or_404(Article, id=id)
    context = {
        'article': article
    }
    return render(
        request,
        'article/article.html',
        context
    )


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
@login_required
def update_state(request, id, state):
    if state not in [c[0] for c in Article.STATE_CHOICES]:
        raise Http404()
    article = get_object_or_404(Article, id=id)
    article.state = state
    article.save()
    return redirect('edit_article', id=id)
