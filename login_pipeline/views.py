# Create your views here.
from django.utils.importlib import import_module
from django.conf import settings
from login_pipeline.exceptions import StopPipeline
from django.utils.http import is_safe_url
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, redirect
from django.template.response import TemplateResponse

PIPELINE = getattr(
    settings,
    'LOGIN_PIPELINE',
    (
        'login_pipeline.pipeline.logout',
        'login_pipeline.pipeline.authenticate',
        'login_pipeline.pipeline.check_email',
    ),
)

MAPPED_PIPELINE = []
for name in PIPELINE:
    mod_name, func_name = name.rsplit('.', 1)
    mod = import_module(mod_name)
    MAPPED_PIPELINE.append(getattr(mod, func_name))


def login(request, *args, **kwargs):

    context = request.session.setdefault(
        'login_pipeline_context',
        {}
    )

    for func in MAPPED_PIPELINE:
        try:
            result = func(request=request, **context) or {}
        except StopPipeline as e:
            raise e

        if isinstance(result, dict):
            context.update(result)
        else:
            return result

    redirect_to = request.REQUEST.get(auth.REDIRECT_FIELD_NAME, '')
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    auth.login(request, context['user'])
    del request.session['login_pipeline_context']

    return HttpResponseRedirect(redirect_to)


def login_form(request):

    if request.method == 'POST':

        form = auth.forms.AuthenticationForm(data=request.POST)

        if form.is_valid():
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            request.session.setdefault('login_pipeline_context', {})['user'] = form.get_user()
            return redirect('login_pipeline')

    else:

        form = auth.forms.AuthenticationForm(request)

    request.session.set_test_cookie()
    return TemplateResponse(
        request,
        'registration/login.html',
        {
            'form': form,
        }
    )
