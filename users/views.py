from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from users.models import User


def list_all(request):
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
        'user/admin.html',
        context
    )


@login_required
def add(request):
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

    return redirect('admin_users', error=error)


@login_required
def delete(request):
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

    return redirect('admin_users')