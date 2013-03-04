from django.contrib.auth.models import AnonymousUser


def pipeline_user(request):

    login_pipeline = request.session.get('login_pipeline')

    if not login_pipeline:
        return AnonymousUser()

    user = login_pipeline['kwargs']['user']

    return user
