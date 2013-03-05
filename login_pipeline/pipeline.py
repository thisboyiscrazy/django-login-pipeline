from django.contrib import auth
User = auth.get_user_model()
from django.template.response import TemplateResponse
from django.contrib import messages
from django.shortcuts import redirect


def logout(request,context):

    if context.get('user'):
        return None

    if request.user.is_authenticated():
        auth.logout(request)

        request.session['login_pipeline_context'] = context


def authenticate(request,context):

    if context.get('user'):
        return None
    
    return redirect('login_pipeline_form')


def check_email(request,context):

    user = context['user']
    user.email = User.objects.get(pk=user.pk).email
    if not user.email:
        request.session['no_email_redirect'] = 'login_pipeline'
        return redirect('no_email')

    return None
