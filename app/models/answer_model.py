from django.db import models
from django.db.models.functions.datetime import Now
from django.contrib.auth.models import User

from app.common.question_info_query import QuestionInfoQuery
from app.models.base_models.base_model import BaseModel
from app.models.question_model import QuestionModel


class AnswerManager(models.Manager):
    def get_best(self):
        return self.filter().order_by('-published_at').order_by('--rating')

    def get_new(self):
        return self.filter().order_by('-published_at')


class AnswerModel(BaseModel):
    text = models.TextField()

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    rating = models.IntegerField(default=0)

    published_at = models.DateTimeField(db_default=Now())

    objects = AnswerManager()
