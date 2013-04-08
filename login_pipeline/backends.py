from login_pipeline.models import PipelineUser
from login_pipeline import next_pipeline_step
from django.contrib.auth import authenticate

from django.contrib.auth import load_backend

class PipelineBackend(object):

    def authenticate(self, skip_pipeline=False, **credentials):

        if skip_pipeline:
            return None

        user = authenticate(skip_pipeline=True, **credentials)
        
        if user == None:
            return None

        user = PipelineUser(user)

        if next_pipeline_step(user):
            return user

        return None

    def get_user(self, pk):
        backend = load_backend(pk['backend'])
        user = backend.get_user(pk['pk'])

        if not user:
            return None

        user.backend = pk['backend']

        return PipelineUser(user)
