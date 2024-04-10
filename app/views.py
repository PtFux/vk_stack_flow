from django.http import HttpResponse
from django.shortcuts import render
from .default_data import *
from .services.behavior import Behavior

_behavior = Behavior()


def get_hot(request):
    number = request.GET.get('page')
    questions = _behavior.get_hot_questions()
    pages, questions = paginate(questions, number)
    return render(request, "hot.html", {
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })


def get_question(request, question_id):
    number = request.GET.get('page', 0)
    item = QUESTIONS[question_id]
    pages, answers = paginate(item.answers, number, per_page=2)
    return render(request, "question.html", {
        "question": item,
        "user": User(),
        "tags": tags,
        "members": members,
        "pages": pages,
        "answers": answers
    })


def get_tag(request, tag_id: int):
    number = request.GET.get('page', 0)
    tag = _behavior.get_tag_by_id(tag_id)
    questions = _behavior.get_questions_by_tag(tag_id)
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
    questions = _behavior.get_new_questions()
    number = request.GET.get('page')
    pages, questions = paginate(questions, number)
    return render(request, "index.html", {
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })
