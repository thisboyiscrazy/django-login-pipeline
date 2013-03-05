from django.contrib import auth
User = auth.get_user_model()
from django.template.response import TemplateResponse
from django.contrib import messages
from django.shortcuts import redirect


def logout(request, user=None, *args, **context):

    if user:
        return {}

    import pdb;pdb.set_trace()
    if request.user.is_authenticated():
        auth.logout(request)

        request.session['login_pipeline_context'] = context


def authenticate(request, user=None, *args, **context):

    if user:
        return {}
    
    return redirect('login_pipeline_form')

def check_email(request, user=None, *args, **context):

    user.email = User.objects.get(pk=user.pk).email
    if not user.email:
        return redirect('no_email')
