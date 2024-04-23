from django.core.paginator import Paginator

from app.common.mappers.map_model_to_logic import MapModelToLogic
from app.models import QuestionModel, TagModel, AnswerModel

from .models import *


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
        return pages, page.start_index(), page.end_index() + 1

    def get_page_and_hot_questions(self, number: int) -> tuple[list[Page], list[Question]]:
        n_questions = self.get_count_all_questions()
        pages, start, end = self._iq_paginate(n_questions, page_number=number)

        hot_questions = self._get_hot_questions_limit(start, end)
        return pages, hot_questions

    def get_page_and_new_questions(self, number: int) -> tuple[list[Page], list[Question]]:
        n_questions = self.get_count_all_questions()
        pages, start, end = self._iq_paginate(n_questions, page_number=number)
        new_questions = self._get_new_questions_limit(start, end)
        return pages, new_questions

    def get_page_and_answers(self, question_id: int, number: int = 0) -> tuple[list[Page], list[Answer]]:
        n_answers = QuestionModel.objects.get(id=question_id).answers.count()
        pages, start, end = self._iq_paginate(n_answers, page_number=number)
        answer_models = QuestionModel.objects.get(id=question_id).answers.all()[start:end]
        answers = [
            self._mapper.map_answer_model_to_logic(answer_model)
            for answer_model in answer_models
        ]
        return pages, answers
