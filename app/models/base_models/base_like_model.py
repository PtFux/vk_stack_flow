from django.db import models

from django.db.models.functions.datetime import Now

from app.models.base_models.base_model import BaseModel


class BaseLikeModel(BaseModel):
    is_positive = models.BooleanField(default=True)

    putted_at = models.DateTimeField(default=Now())

    class Meta:
        abstract = True
