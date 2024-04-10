from app.common.mappers.map_model_to_logic import MapModelToLogic
from app.models import QuestionModel, TagModel


class Behavior:
    def __init__(self):
        self._mapper = MapModelToLogic()

    def get_hot_questions(self) -> list:
        hot_questions = [
            self._mapper.map_question_model_to_logic(question_model)
            for question_model in QuestionModel.objects.get_hot().all()
        ]
        return hot_questions

    def get_new_questions(self):
        new_questions = [
            self._mapper.map_question_model_to_logic(question_model)
            for question_model in QuestionModel.objects.get_new().all()
        ]
        return new_questions

    def get_questions_by_tag(self, tag_id: int):
        questions_by_tag = [
            self._mapper.map_question_model_to_logic(question_model)
            for question_model in QuestionModel.objects.get_by_tag_id(tag_id).all()
        ]
        return questions_by_tag

    def get_question_by_id(self, question_id: int):
        pass

    def get_tag_by_id(self, tag_id: int):
        return self._mapper.map_tag_model_to_logic(
            TagModel.objects.filter(id=tag_id).get()
        )
