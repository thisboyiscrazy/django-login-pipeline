from login_pipeline.models import PipelineUser
from login_pipeline import next_pipeline_step
from django.contrib.auth import login
from django.contrib.auth import load_backend

class LoginPipelineMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):

        if hasattr(view_func,"login_pipeline_view") and view_func.login_pipeline_view:
            return None

        if not isinstance(request.user,PipelineUser):
            return None

        if request.session.get('BYPASS_LOGIN_PIPELINE'):
            return None

        next_step = next_pipeline_step(request.user)

        if next_step:
            return next_step

        backend = load_backend(request.user.pk['backend'])
        user = backend.get_user(request.user.pk['pk'])
        login(request,user)
