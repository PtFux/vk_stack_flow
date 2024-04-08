from django.db import models
from django.db.models.functions.datetime import Now

from app.common.question_info_query import QuestionInfoQuery
from app.models.tag_model import TagModel
from app.models.base_models.base_model import BaseModel


class QuestionManager(models.Manager):
    def get_hot(self,
                rating: int = QuestionInfoQuery.REALLY_HOT_QUESTION_RATING,
                limit: int = QuestionInfoQuery.LIMIT_HOT_QUESTION):
        return self.filter(rating__gte=rating).order_by('-rating')[:limit]

    def get_new(self):
        return self.filter().order_by('-published_at')

    def get_by_tag(self, tag):
        return self.filter(tag=tag)


class QuestionModel(BaseModel):
    title = models.CharField(max_length=100)
    text = models.TextField()

    tags = models.ManyToManyField(TagModel, related_name='questions')
    n_answers = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    published_at = models.DateTimeField(db_default=Now())

    objects = QuestionManager()

    def __str__(self):
        return self.title
