from datetime import datetime

from django.contrib.auth.views import UserModel
from django.core.paginator import Paginator
from django.http import HttpRequest

from app.common.mappers.map_model_to_logic import MapModelToLogic
from app.models import QuestionModel, TagModel, AnswerModel, ProfileModel

from .models import *

import logging

logger = logging.getLogger(__name__)

module_logging_info = {
    "module_name": "behavior.py",
    "level_mvp": "logic",
    "level": "INFO"
}


class Behavior:
    def __init__(self):
        self._mapper = MapModelToLogic()

    def _get_hot_questions_limit(self, start: int = 0, end: int = None) -> list[Question]:
        hot_questions = [
            self._mapper.map_question_model_to_logic(question_model)
            for question_model in QuestionModel.objects.get_hot(start=start, end=end).all()
        ]
        return hot_questions

    def _get_new_questions_limit(self, start: int, end: int) -> list[Question]:
        new_questions = [
            self._mapper.map_question_model_to_logic(question_model)
            for question_model in QuestionModel.objects.get_new(start, end).all()
        ]
        return new_questions

    def _get_questions_by_tag(self, tag_id: int, start: int = 0, end: int = None) -> list[Question]:
        questions_by_tag = [
            self._mapper.map_question_model_to_logic(question_model)
            for question_model in QuestionModel.objects.get_by_tag_id(tag_id, start, end).all()
        ]
        return questions_by_tag

    def get_question_by_id(self, question_id: int) -> Question:
        return self._mapper.map_question_model_to_logic(
            QuestionModel.objects.get_question_by_id(question_id).get()
        )

    def get_tag_by_id(self, tag_id: int) -> Tag:
        return self._mapper.map_tag_model_to_logic(
            TagModel.objects.filter(id=tag_id).get()
        )

    def get_tag_model_by_id(self, tag_id: int) -> TagModel:
        return TagModel.objects.filter(id=tag_id).get()

    @staticmethod
    def get_count_all_questions() -> int:
        return QuestionModel.objects.count()

    @staticmethod
    def get_count_questions_by_tag(tag_id: int) -> int:
        return TagModel.objects.filter(id=tag_id).count()

    @staticmethod
    def __get_int_number(number: int | str, default: int = 1) -> int:
        try:
            number = int(number)
        except ValueError:
            number = default
        except TypeError:
            number = default
        number = max(1, number)
        return number

    def _iq_paginate(self, n_objects: int, page_number=1, per_page=3) -> tuple[list[Page], int, int]:
        """
        Paginate function.
        Use django paginate to create custom Page (for templates) and start  and end index
            by object's num, page_number, per_page.
        params:
            n_objects: number of objects to paginate
            page_number: page number
            per_page: number of objects per page
        return:
            pages: custom Page objects (for templates)
            start: int - index of first element in current Page*
            end: int - index of last element in current Page
        * Numerate from 0.
        """

        page_number = self.__get_int_number(page_number)

        some_list = [0] * n_objects
        page_obj = Paginator(some_list, per_page)
        number = min(page_number, page_obj.num_pages)
        page = page_obj.get_page(number)

        pages = [
            Page(
                number=p if type(p) == int else 0,
                title=str(p),
                is_active=True if p == number else False,
                is_number=True if type(p) == int else False
            ) for p in page_obj.get_elided_page_range(number, on_each_side=1, on_ends=2)
        ]

        start = max(0, page.start_index() - 1)
        return pages, start, page.end_index()

    def get_page_and_hot_questions(self, number: int) -> tuple[list[Page], list[Question]]:
        n_questions = self.get_count_all_questions()
        pages, start, end = self._iq_paginate(n_questions, page_number=number)
        hot_questions = self._get_hot_questions_limit(start, end)
        self.logging_info(f"Get question hot {number} start {start} end {end} n_questions {n_questions}",
                          **module_logging_info)
        return pages, hot_questions

    def get_page_and_new_questions(self, number: int) -> tuple[list[Page], list[Question]]:
        n_questions = self.get_count_all_questions()
        pages, start, end = self._iq_paginate(n_questions, page_number=number)
        new_questions = self._get_new_questions_limit(start, end)
        self.logging_info(f"Get question new {number} start {start} end {end} n_questions {n_questions}",
                          **module_logging_info)
        return pages, new_questions

    def get_page_questions_by_tag(self, tag_id: int, number: int = 0) -> tuple[list[Page], list[Question]]:
        n_questions = QuestionModel.objects.filter(tags__id=tag_id).count()

        pages, start, end = self._iq_paginate(n_questions, page_number=number)
        new_questions = QuestionModel.objects.get_by_tag_id(tag_id, start, end)
        questions_by_tag = [
            self._mapper.map_question_model_to_logic(question_model)
            for question_model in new_questions
        ]
        self.logging_info(f"Get question by TAG {tag_id} start {start} end {end} n_questions {n_questions}",
                          **module_logging_info)
        return pages, questions_by_tag

    def get_page_and_answers(self, question_id: int, number: int = 0) -> tuple[list[Page], list[Answer]]:
        n_answers = QuestionModel.objects.get(id=question_id).answers.count()
        pages, start, end = self._iq_paginate(n_answers, page_number=number)
        answer_models = QuestionModel.objects.get(id=question_id).answers.all()[start:end]
        answers = [
            self._mapper.map_answer_model_to_logic(answer_model)
            for answer_model in answer_models
        ]
        self.logging_info(
            f"Get answers by num {number} question {question_id} start {start} end {end} n_answers {n_answers}",
            **module_logging_info
        )
        return pages, answers

    @staticmethod
    def get_auth_user(request) -> UserModel:
        return request.user

    def create_user_with_profile(self, login: str, email: str, password: str, avatar=None, **kwargs) -> UserModel:
        user = UserModel.objects.create_user(
            username=login, email=email, password=password
        )
        user.save()
        profile = ProfileModel(user=user, avatar=avatar)
        profile.save()
        self.logging_info(f"Created user model {user.username} and profile model {profile}",
                          **module_logging_info)
        return user

    def update_user_and_profile(self, user: UserModel, username: str, email: str, upload_avatar: str = None, **kwargs):
        if username:
            user.username = username
        if email:
            user.email = email
        if upload_avatar:
            profile = ProfileModel.objects.get(user=user)
            profile.avatar = upload_avatar
            profile.save()
        else:
            profile = None
        user.save()
        self.logging_info(f"Updated user model '{user.username}' and profile model '{profile}'", **module_logging_info)

    def create_question(self,
                        user: UserModel, title: str, text: str, tags: list[int] = None, new_tags: list[int] = None,
                        **kwargs) -> QuestionModel:
        add_tags = []
        if new_tags:
            new_tags_models = []
            for tag in new_tags:
                tag_model = TagModel(title=tag)
                tag_model.save()
                new_tags_models.append(tag_model)
            add_tags.extend(new_tags_models)
            self.logging_info(f"Created tag models {new_tags_models}", **module_logging_info)
        if tags:
            tag_models = [self.get_tag_model_by_id(tag_id) for tag_id in tags]
            add_tags.extend(tag_models)

        question = QuestionModel(user=user, title=title, text=text)
        question.save()
        question.tags.add(*add_tags)
        question.save()
        self.logging_info(f"Created question model {question.id}", **module_logging_info)
        return question

    def get_tags_model(self) -> list[TagModel]:
        tags = TagModel.objects.all()
        return tags

    def create_answer_by_question_id(self, user: UserModel, question_id: str, text: str, **kwargs) -> AnswerModel:
        question = QuestionModel.objects.get(id=question_id)
        answer = AnswerModel(user=user, question=question, text=text)
        answer.save()
        self.logging_info(f"Created answer {answer.id}", **module_logging_info)
        return answer

    def get_page_and_answers_by_answer(self, question_id: str, answer_id: str) -> tuple[list[Page], list[Answer]]:
        answer_models = QuestionModel.objects.get(id=question_id).answers.all()
        answer = answer_models.get(id=answer_id)
        answer_models = list(answer_models)

        number = (answer_models.index(answer) + 3) // 3    # number page with current answer

        pages, start, end = self._iq_paginate(len(answer_models), page_number=number)
        answer_models_in_page = answer_models[start:end]

        answers_in_page = [
            self._mapper.map_answer_model_to_logic(answer_model)
            for answer_model in answer_models_in_page
        ]
        self.logging_info(f"Get {len(answers_in_page)} answers by answer {answer_id} start {start} end {end}",
                          **module_logging_info)
        return pages, answers_in_page

    @staticmethod
    def logging_info(message: str, module_name: str, level_mvp: str, level: str):
        logger.warning(f"{level} | [{datetime.now()}] [{level_mvp}-{module_name}]: {message}")

    @staticmethod
    def get_tags_and_members():
        from ..default_data import tags, members

        return tags, members
