from django.contrib.auth.models import User
from django.db import models

from django.db.models.functions.datetime import Now

from app.models.base_models.base_like_model import BaseLikeModel
from app.models.question_model import QuestionModel


class QuestionLikeModel(BaseLikeModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='question_likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_question_like'),
        ]
