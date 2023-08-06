from django.db.models.manager import Manager
from django.http import Http404
from django.template.loader import render_to_string
from django.conf import settings


def get_object_or_404(self, error_text='Page is can not be found', **kwargs):
    try:
        return self.get(**kwargs)
    except self.model.DoesNotExist:
        raise  Http404(error_text)


Manager.get_object_or_404 = get_object_or_404