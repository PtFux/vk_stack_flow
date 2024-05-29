from django.db import models
from django.db.models import QuerySet
from django.db.models.functions.datetime import Now
from django.contrib.auth.models import User

from app.common.question_info_query import QuestionInfoQuery
from app.models.tag_model import TagModel
from app.models.base_models.base_model import BaseModel


class QuestionManager(models.Manager):
    def get_hot(self,
                rating: int = QuestionInfoQuery.REALLY_HOT_QUESTION_RATING,
                start: int = 0,
                end: int = QuestionInfoQuery.LIMIT_HOT_QUESTION) -> QuerySet:
        return self.filter(rating__gte=rating).order_by('-rating', '-published_at').all()[start:end]

    def get_new(self, start: int = 0, end: int = None) -> QuerySet:
        end = end or self.count()
        return self.filter().order_by('-published_at', '-rating').all()[start:end]

    def get_by_tag_id(self, tag_id: int, start: int = 0, end: int = None) -> QuerySet:
        end = end or self.filter(tags__id=tag_id).count()
        return self.filter(tags__id=tag_id).all()[start:end]

    def get_question_by_id(self, question_id: int) -> QuerySet:
        return self.filter(id=question_id)


class QuestionModel(BaseModel):
    title = models.CharField(max_length=100)
    text = models.TextField()

    tags = models.ManyToManyField(TagModel, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    n_answers = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    published_at = models.DateTimeField(db_default=Now())

    objects = QuestionManager()

    def __str__(self):
        return self.title
