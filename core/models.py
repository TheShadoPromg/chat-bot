from abc import abstractmethod

import shortuuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.managers import SoftDeletableManager
from model_utils.models import TimeStampedModel, SoftDeletableModel


def get_unique_id():
    return shortuuid.random(length=16)


class BaseModel(TimeStampedModel, SoftDeletableModel, models.Model):
    active = SoftDeletableManager()
    unique_id = models.CharField(verbose_name=_('Unique ID'), max_length=16, default=get_unique_id, editable=False,
                                 unique=True)

    @staticmethod
    @abstractmethod
    def get_reference_type():
        raise NotImplemented()

    @property
    def reference_code(self):
        if not self.pk:
            raise ValueError('Cannot get reference until object is saved')

        reference_number = str(self.pk).zfill(8)
        return f'{self.get_reference_type()}{reference_number}'

    class Meta:
        abstract = True
        default_manager_name = 'active'
