from django.contrib import auth
User = auth.get_user_model()
from django.template.response import TemplateResponse
from django.contrib import messages
from django.shortcuts import redirect


def check_email(user):

    user.email = User.objects.get(pk=user.pk).email
    if not user.email:
        return 'account/no_email/'

    return None
