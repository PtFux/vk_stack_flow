from app.models import QuestionModel, TagModel, AnswerModel
from app.services.models import Answer
from app.services.models.question import Question
from app.services.models.tag import Tag


class MapModelToLogic:

    def map_question_model_to_logic(self, model: QuestionModel) -> Question:
        question = Question(
            question_id=int(model.id),
            title=model.title,
            text=model.text,
            n_answers=model.n_answers,
            rating=0
        )
        question.tags = [self.map_tag_model_to_logic(tag)
                         for tag in model.tags.all()
                         ]
        question.answers = [
            self.map_answer_model_to_logic(answer)
            for answer in model.answers.all()
        ]
        question.n_answers = model.n_answers or len(question.answers)
        return question

    @staticmethod
    def map_question_logic_to_map(logic: Question) -> QuestionModel:
        pass

    @staticmethod
    def map_tag_model_to_logic(model: TagModel) -> Tag:
        tag = Tag(
            tag_id=int(model.id),
            title=model.title,
        )
        return tag

    @staticmethod
    def map_answer_model_to_logic(model: AnswerModel) -> Answer:
        answer = Answer(
            id=model.id,
            text=model.text,
            rating=model.rating
        )
        return answer
