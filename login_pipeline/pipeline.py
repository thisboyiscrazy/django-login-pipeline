from django.contrib import auth
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

def logout(request,index,*args,**kwargs):

    if request.user.is_authenticated():
        auth.logout(request)

        request.session['login_pipeline'] = {
            'index': index,
            'args':args,
            'kwargs':kwargs,
        }

def authenticate(request,*args,**kwargs):
    
    if request.method == "POST":
        
        form = auth.forms.AuthenticationForm(data=request.POST)

        if form.is_valid():
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return {'user':form.get_user()}

    else:

        form = auth.forms.AuthenticationForm(request)

    request.session.set_test_cookie()
    return TemplateResponse(
        request,
        'registration/login.html',
        {
            'form':form,
        }
    )

def check_email(request, user=None, *args, **kwargs):

    if not user.email:
        return redirect("no_email")
