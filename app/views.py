from django.http import HttpResponse
from django.shortcuts import render
from .default_data import *


def index(request):
    return render(request, 'index.html', {
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": QUESTIONS
    })


def get_hot(request, number: int = 1):
    pages, questions = paginate(QUESTIONS, number)
    return render(request, "hot.html", {
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })


def get_question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, "question.html", {
        "question": item,
        "user": User(),
        "tags": tags,
        "members": members,
    })


def get_tag(request, tag_id: str):
    return HttpResponse(tag_id)


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


def get_page(request, number: str = "1"):
    try:
        number = int(number)
    except ValueError:
        number = 1

    pages, questions = paginate(QUESTIONS, number)
    return render(request, "index.html", {
        "user": User(),
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })
