from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
User = get_user_model()


def pipeline_user(request):

    if request.user.is_authenticated():
        return request.user

    context = request.session.get('login_pipeline_context')

    if not context:
        return AnonymousUser()

    user = context.get('user') or AnonymousUser()

    return user
