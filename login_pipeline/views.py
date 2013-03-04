# Create your views here.
from django.utils.importlib import import_module
from django.conf import settings
from login_pipeline.exceptions import StopPipeline


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
    MAPPED_PIPELINE.append(getattr(mod,func_name))


def login(request, *args, **kwargs):

    login_pipeline = request.session.setdefault(
            'login_pipeline',
            {
                'index': 0,
                'args':args,
                'kwargs':kwargs,
            }
    )

    for idx, func in enumerate(MAPPED_PIPELINE, login_pipeline['index']):
        try:
            result = func(request,*args,index=idx,**kwargs) or {}
        except StopPipeline:
            return kwargs

        if isinstance(result, dict):
            kwargs.update(result)
        else:
            return result

        login_pipeline['index'] = idx

    import pdb;pdb.set_trace()
    return kwargs
