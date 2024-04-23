from django.http import HttpResponse
from django.shortcuts import render
from .default_data import *
from .services.behavior import Behavior

_behavior = Behavior()


def get_hot(request):
    number = request.GET.get('page')
    pages, questions = _behavior.get_page_and_hot_questions(number)
    print(questions)
    return render(request, "hot.html", {
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })


def get_question(request, question_id):
    number = request.GET.get('page', 0)
    question = _behavior.get_question_by_id(question_id)
    pages, answers = _behavior.get_page_and_answers(question_id, number)
    return render(request, "question.html", {
        "question": question,
        "user": User(),
        "tags": tags,
        "members": members,
        "pages": pages,
        "answers": answers
    })


def get_tag(request, tag_id: int):

    user = _behavior.get_auth_user()
    tags, members = _behavior.get_tags_members_for_column()
    ## долделать!!!

    number = request.GET.get('page', 0)
    tag = _behavior.get_tag_by_id(tag_id)
    questions = _behavior._get_questions_by_tag(tag_id)
    pages, questions = paginate(questions, number)
    return render(request, "tag.html", {
        "tag": tag,
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })


def get_login(request):
    return render(request, "login.html",
                  context={
                      "tags": tags,
                      "members": members,
                  })


def get_signup(request):
    return render(request, "signup.html",
                  context={
                      "tags": tags,
                      "members": members,
                  })


def get_ask(request):
    return render(request, "ask.html",
                  context={
                      "tags": tags,
                      "members": members,
                  })


def get_settings(request):
    return render(request, "settings.html",
                  context={
                      "tags": tags,
                      "members": members,
                  })


def get_member(request, user_id: int):
    return HttpResponse(f"{user_id}")


def get_page(request):
    number = request.GET.get('page')
    pages, questions = _behavior.get_page_and_new_questions(number)
    return render(request, "index.html", {
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })
