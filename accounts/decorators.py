from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


def unauth_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if (request.user.is_authenticated):
            messages.info(request, 'you ready autheticated')
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allow_users(allow_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if (request.user.groups.exists()):
                group = request.user.groups.all()[0].name

            if (group in allow_roles):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("you not allow to the access this page")

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if (request.user.groups.exists()):
            group = request.user.groups.all()[0].name

        if (group == 'customer'):
            return redirect('user_page')

        if (group == 'admin'):
            return view_func(request, *args, **kwargs)

    return wrapper_func
