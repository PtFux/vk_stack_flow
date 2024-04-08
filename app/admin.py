from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.ProfileModel)
admin.site.register(models.QuestionModel)
admin.site.register(models.AnswerModel)
admin.site.register(models.TagModel)
admin.site.register(models.QuestionLikeModel)
admin.site.register(models.AnswerLikeModel)
