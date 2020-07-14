from django.db.models import Model as DjangoModel, DateTimeField
from django.forms.models import model_to_dict
from django.utils import timezone
from django.db.models import * # so we can rested import models


class Model(DjangoModel):

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, values=None, **kwargs):
        values = values or kwargs
        return cls.objects.create(**values)

    def update(self, values=None, **kwargs):
        values = values or kwargs
        for field in list(values.keys()):
            setattr(self, field, values[field])
        return self

    def to_dict(self, *args, **kwargs):
        return model_to_dict(self, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        return self
