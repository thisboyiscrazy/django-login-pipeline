from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
User = get_user_model()

from functools import wraps

from django.conf import settings
from django.utils.importlib import import_module

from django.utils.decorators import available_attrs


def get_pipeline():
    pipeline = []
    for name in settings.LOGIN_PIPELINE:
        mod_name, func_name = name.rsplit('.', 1)
        mod = import_module(mod_name)
        pipeline.append(getattr(mod, func_name))

    return pipeline


def next_pipeline_step(user):

    for func in get_pipeline():

        result = func(user)

        if result:
            return result

    return None


def pipeline_user(request):

    if request.user.is_authenticated():
        return request.user

    context = request.session.get('login_pipeline_context')

    if not context:
        return AnonymousUser()

    user = context.get('user') or AnonymousUser()

    return user


def login_pipeline_view(view_func):
    """
    Marks a view function as being exempt from the CSRF view protection.
    """
    # We could just do view_func.csrf_exempt = True, but decorators
    # are nicer if they don't have side-effects, so we return a new
    # function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.login_pipeline_view = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
