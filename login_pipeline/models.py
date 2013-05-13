from django.contrib.auth import load_backend

class PipelineUser(object):

    def __init__(self,user=None):
        self.__dict__['_user'] = user
        self.__dict__['pk'] = {"pk":user.pk,"backend":user.backend}

    def __getattr__(self, name):
        if name == 'pk':
            return self.pk

        return getattr(self._user,name)

    def __setattr__(self, name, value):
        if name == 'pk':
            return

        setattr(self._user,name,value)

    def __unicode__(self):
        return self._user.__unicode__()
