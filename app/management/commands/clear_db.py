from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.models import *
from ._data_for_fill_db import *


class Command(BaseCommand):
    help = 'This command clear the database'

    def add_arguments(self, parser):
        parser.add_argument('-dt', '--datetime', type=datetime, default=datetime.now(), required=False,
                            help='Дата, созданные записи до которой, будут удалены')

        parser.add_argument('-m', '--massacre', type=bool, default=False, required=False,
                            help='Удаление всех данных в базе')

    def handle(self, *args, **options):
        native_time: datetime = options.get('datetime', datetime.now())
        time = make_aware(native_time)
        self.__delete_users(time)
        self.__delete_tags(time)
        self.__delete_questions(time)
        self.__delete_answers(time)
        self.__delete_question_likes(time)
        self.__delete_answer_likes(time)

        if options.get('massacre', False):
            self.__delete_all()

    @staticmethod
    def __delete_users(time: datetime):
        User.objects.filter(date_joined__gte=time).delete()

    @staticmethod
    def __delete_tags(time: datetime):
        TagModel.objects.filter(created_at__gte=time).delete()

    @staticmethod
    def __delete_questions(time: datetime):
        QuestionModel.objects.filter(created_at__gte=time).delete()

    @staticmethod
    def __delete_answers(time: datetime):
        AnswerModel.objects.filter(created_at__gte=time).delete()

    @staticmethod
    def __delete_question_likes(time: datetime):
        QuestionLikeModel.objects.filter(created_at__gte=time).delete()

    @staticmethod
    def __delete_answer_likes(time: datetime):
        AnswerLikeModel.objects.filter(created_at__gte=time).delete()

    @staticmethod
    def __delete_all():
        User.objects.all().delete()
        TagModel.objects.all().delete()
        QuestionModel.objects.all().delete()
        AnswerModel.objects.all().delete()
        QuestionLikeModel.objects.all().delete()
        AnswerLikeModel.objects.all().delete()
