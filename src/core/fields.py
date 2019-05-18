import uuid

from django.db import models


class UUIDPrimaryKey(models.UUIDField):

    def __init__(self, **kwargs):
        kwargs['primary_key'] = True
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', uuid.uuid4)
        super().__init__(**kwargs)
