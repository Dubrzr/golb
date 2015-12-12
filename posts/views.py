from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from blog.views import admin
from posts.models import Article, History


def all_articles(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(
        request,
        'all_articles.html',
        context
    )



@login_required
def editor(request, error=None):
    context = {
        'articles': Article.objects.all(),
        'error': error,
        'languages': Article.LANGUAGES_CHOICES
    }
    return render(
        request,
        'admin_articles.html',
        context
    )


@login_required
def add_article(request):
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
    return redirect('editor')


@login_required
def edit_article(request, id, history_id=None):
    article = get_object_or_404(Article, id=id)
    if request.POST:
        article_data = {
            'title': request.POST.get('title'),
            'contents': request.POST.get('contents'),
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
        'contents': history.get_contents()
    }
    return render(
        request,
        'editor.html',
        context
    )


@login_required
def del_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.state = 'RE'
    article.save()


@login_required
def history_article(request, id):
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
        'article_history.html',
        context
    )


def article(request, id):
    article = get_object_or_404(Article, id=id)
    context = {
        'article': article
    }
    return render(
        request,
        'article.html',
        context
    )
