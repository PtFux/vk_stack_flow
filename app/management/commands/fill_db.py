from random import choice

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.models import *
from ._data_for_fill_db import *


class Command(BaseCommand):
    help = 'This command fills the database'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--ratio', type=int, default=10000, required=False,
                            help='The number of users to be created')

    def handle(self, *args, **options):
        print(options['ratio'])
        ratio = options.get('ratio', 0)
        self.__create_tags(ratio)
        print("Tags created")
        self.__create_users(ratio)
        print("Users created")
        self.__create_questions(ratio)
        print("Questions created")
        self.__create_answers(ratio)
        print("Answers created")
        self.__create_likes_questions(100 * ratio)
        print("Likes questions created")
        self.__create_likes_answers(100 * ratio)
        print("Likes answers created")

        self.__add_tags_for_questions()
        print("Tags and questions joined")

    @staticmethod
    def __create_tags(n_tags: int):
        new_tags = [
            TagModel(title=TagsData.get_title(i))
            for i in range(n_tags)
        ]
        TagModel.objects.bulk_create(new_tags)

    @staticmethod
    def __create_users(n_users: int):
        new_users = []
        for i in range(n_users):
            temp_user = User(
                username=UsersData.get_username(i),
                email=UsersData.get_emails(i),
                password=UsersData.get_passwords(i),
            )
            new_users.append(temp_user)

        User.objects.bulk_create(new_users)

    @staticmethod
    def __create_questions(n_questions: int):
        users = User.objects.all()
        new_questions = []
        for i in range(n_questions):
            temp_question = QuestionModel(
                title=QuestionsData.get_title(i),
                text=QuestionsData.get_text(i),
                user=users[i % len(users)],
            )
            new_questions.append(temp_question)
        QuestionModel.objects.bulk_create(new_questions)

    @staticmethod
    def __create_answers(n_answers: int):
        users = User.objects.all()
        questions = QuestionModel.objects.all()
        new_answers = []
        for i in range(n_answers):
            temp_answer = AnswerModel(
                text=AnswersData.get_text(i),
                question=questions[i % len(questions)],
                user=users[i % len(users)],
            )
            new_answers.append(temp_answer)

        AnswerModel.objects.bulk_create(new_answers)

    @staticmethod
    def __create_likes_questions(n_likes: int):
        users = User.objects.all()
        questions = QuestionModel.objects.all()
        pair_user_question = set()
        n_tries = 0
        while len(pair_user_question) < n_likes and n_tries < 100:
            n_tries += 1
            pair_user_question.add((choice(users), choice(questions)))

        new_likes = []
        for pair in pair_user_question:
            temp_like = QuestionLikeModel(
                user=pair[0],
                question=pair[1],
            )
            new_likes.append(temp_like)
        QuestionLikeModel.objects.bulk_create(new_likes)

    @staticmethod
    def __create_likes_answers(n_likes: int):
        users = User.objects.all()
        answers = AnswerModel.objects.all()
        pair_user_answer = set()
        n_tries = 0
        while len(pair_user_answer) < n_likes and n_tries < 10:
            n_tries += 1
            pair_user_answer.add((choice(users), choice(answers)))

        new_likes = []
        for pair in pair_user_answer:
            temp_like = AnswerLikeModel(
                user=pair[0],
                answer=pair[1],
            )
            new_likes.append(temp_like)
        AnswerLikeModel.objects.bulk_create(new_likes)

    @staticmethod
    def __add_tags_for_questions():
        questions = QuestionModel.objects.all()
        tags = TagModel.objects.all()
        for i in range(tags.count()):
            temp_tag = tags[i]
            temp_tag.questions.add(*questions[(i % len(questions)):(i + 5) % len(questions)])
