from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from blog.quotes.models import Quote
from blog.decorators import never_ever_cache


@login_required
@never_ever_cache
def admin(request, error=None):
    context = {
        'quotes': Quote.objects.all(),
        'error': error
    }
    return render(
        request,
        'quotes/admin.html',
        context
    )


@login_required
@never_ever_cache
def add(request):
    error = None
    if request.POST:
        article_data = {
            'contents': request.POST.get('contents'),
            'author': request.POST.get('author'),
            'added_by': request.user
        }
        if None in [k for v, k in article_data.items()]:
            error = 'Veuillez remplir tous les champs.'
        else:
            try:
                Quote.objects.create(**article_data)
            except Exception as e:
                error = 'Champs invalides. ({})'.format(e)

    if error:
        return admin(request, error)
    return admin(request)


@login_required
@never_ever_cache
def delete(request):
    if request.GET:
        quote_id = request.GET.get('quote_id')
        try:
            quote = get_object_or_404(Quote, id=quote_id)
        except:
            raise Http404()
        quote.delete()

    return admin(request)