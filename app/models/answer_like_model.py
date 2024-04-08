from django.contrib.auth.models import User
from django.db import models

from django.db.models.functions.datetime import Now

from app.models.answer_model import AnswerModel
from app.models.base_models.base_like_model import BaseLikeModel


class AnswerLikeModel(BaseLikeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(AnswerModel, on_delete=models.CASCADE, related_name="answer_likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_answer_like'),
        ]
