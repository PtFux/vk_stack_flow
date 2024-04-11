from random import choice, randint

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
        self._create_tags(ratio)
        print("Tags created")
        self._create_users(ratio)
        print("Users created")
        self._create_questions(10 * ratio)
        print("Questions created")
        self._create_answers(100 * ratio)
        print("Answers created")
        self._create_likes_questions(100 * ratio)
        print("Likes questions created")
        self._create_likes_answers(100 * ratio)
        print("Likes answers created")

        self._add_tags_for_questions()
        print("Tags and questions joined")

    @staticmethod
    def _create_tags(n_tags: int):
        new_tags = [
            TagModel(title=TagsData.get_title(i))
            for i in range(n_tags)
        ]
        TagModel.objects.bulk_create(new_tags)

    @staticmethod
    def _create_users(n_users: int):
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
    def _create_questions(n_questions: int):
        users = User.objects.all()
        new_questions = []
        for i in range(n_questions):
            temp_question = QuestionModel(
                title=QuestionsData.get_title(i),
                text=QuestionsData.get_text(i),
                user=users[i % len(users)],
                rating=randint(0, 100)
            )
            new_questions.append(temp_question)
        QuestionModel.objects.bulk_create(new_questions)

    @staticmethod
    def _create_answers(n_answers: int):
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

    def _create_likes_questions(self, n_likes: int):
        users = User.objects.all()
        questions = QuestionModel.objects.all()

        pair_user_question = self.__get_random_unique_pairs(n_likes, questions, users)

        new_likes = []
        for pair in pair_user_question:
            temp_like = QuestionLikeModel(
                user=pair[0],
                question=pair[1],
            )
            new_likes.append(temp_like)
        QuestionLikeModel.objects.bulk_create(new_likes)

    def _create_likes_answers(self, n_likes: int):
        users = User.objects.all()
        answers = AnswerModel.objects.all()

        pair_user_answer = self.__get_random_unique_pairs(n_likes, users, answers)

        new_likes = []
        for pair in pair_user_answer:
            temp_like = AnswerLikeModel(
                user=pair[0],
                answer=pair[1],
            )
            new_likes.append(temp_like)
        AnswerLikeModel.objects.bulk_create(new_likes)

    @staticmethod
    def _add_tags_for_questions():
        questions = QuestionModel.objects.all()
        tags = TagModel.objects.all()
        for i in range(questions.count()):
            temp_questions = questions[i]
            temp_questions.tags.add(*tags[(i % len(tags)):(i + 3) % len(tags)])

    @staticmethod
    def __get_random_unique_pairs(n_pairs: int, objs_1, objs_2) -> set:
        uniq_pairs = set()
        n_tries = 0
        while len(uniq_pairs) < n_pairs and n_tries < 10:
            n_tries += 1
            uniq_pairs.add((choice(objs_1), choice(objs_2)))

        return uniq_pairs
