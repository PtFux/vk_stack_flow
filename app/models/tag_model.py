from django.db import models

from app.models.base_models.base_model import BaseModel


class TagModel(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
