from django.contrib.auth.models import User
from django.db import models

from app.models.base_models.base_model import BaseModel


class ProfileModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)
