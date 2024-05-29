from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .services.behavior import Behavior
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.contrib import auth

from .services.forms import *

_behavior = Behavior()

module_logging_info = {
    "module_name": "views.py",
    "level_mvp": "front+logic",
    "level": "INFO"
}


def get_hot(request):
    number = request.GET.get('page')
    pages, questions = _behavior.get_page_and_hot_questions(number)
    user = _behavior.get_auth_user(request)

    tags, members = _behavior.get_tags_and_members()
    return render(request, "hot.html", {
        "user": user,
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })


def get_question(request, question_id):
    user = _behavior.get_auth_user(request)
    question = _behavior.get_question_by_id(question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES)
        if user.is_authenticated:
            if form.is_valid():
                answer = _behavior.create_answer_by_question_id(user, question_id, **form.cleaned_data)
                response = redirect(reverse("question", kwargs={'question_id': question_id}))
                response['Location'] += f'?answer_id={answer.id}'
                response['Location'] += f'#{answer.id}'

                _behavior.logging_info(f"Views debug: redirect to {response.url}", **module_logging_info)
                return response
        else:
            form.add_error(field=None, error="You are not logged in.")
    else:
        form = AnswerForm()

    number = request.GET.get('page', 0)
    answer_id = request.GET.get('answer_id')
    if answer_id:
        pages, answers = _behavior.get_page_and_answers_by_answer(question_id, answer_id)
    else:
        pages, answers = _behavior.get_page_and_answers(question_id, number)

    tags, members = _behavior.get_tags_and_members()
    return render(request, "question.html", {
        "question": question,
        "user": user,
        "tags": tags,
        "members": members,
        "pages": pages,
        "answers": answers,
        "form": form
    })


def get_tag(request, tag_id: int):
    user = _behavior.get_auth_user(request)

    number = request.GET.get('page', 0)
    tag = _behavior.get_tag_by_id(tag_id)
    pages, questions = _behavior.get_page_questions_by_tag(tag_id, number)

    tags, members = _behavior.get_tags_and_members()
    return render(request, "tag.html", {
        "tag": tag,
        "user": user,
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })


def logout(request, url: str):
    user = request.user
    if user is not None:
        auth.logout(request)
        _behavior.logging_info(f"Logged out {user.username}", **module_logging_info)
    return redirect(url)


@require_http_methods(['GET', 'POST'])
def login(request):
    tags, members = _behavior.get_tags_and_members()
    user = request.user
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                continue_url = request.GET.get('next', reverse('main'))
                _behavior.logging_info(f"Login successful redirect  to {continue_url}", **module_logging_info)
                return redirect(continue_url)
            else:
                form.add_error(field=None, error="User login error!")
        _behavior.logging_info(f"Login failed {form.errors}", **module_logging_info)
    else:
        form = LoginForm()
        next = request.GET.get('next', reverse("main"))
        return render(request, "login.html", context={
              "tags": tags,
              "user": user,
              "members": members,
              "form": form,
              "next": next
          })

    next = request.GET.get('next', reverse('main'))
    return render(request, "login.html", context={
        "user": user,
        "tags": tags,
        "members": members,
        "form": form,
        "next": next
    })


@require_http_methods(['GET', 'POST'])
@csrf_protect
def signup(request):
    tags, members = _behavior.get_tags_and_members()
    user = request.user
    if request.user.is_authenticated:
        return redirect(reverse("main"))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = _behavior.create_user_with_profile(**form.cleaned_data)
            auth_login(request, user)
            return redirect(reverse("main"))
    else:
        form = RegisterForm()
        return render(request, "signup.html",
                      context={
                          "user": user,
                          "tags": tags,
                          "members": members,
                          "form": form
                      })
    return render(request, "signup.html",
                  context={
                      "user": user,
                      "form": form,
                      "tags": tags,
                      "members": members,
                  })


@login_required(login_url="login")
@csrf_protect
def ask(request):
    user = _behavior.get_auth_user(request)
    tags = _behavior.get_tags_model()
    tags_for_ask = [(tag.id, tag.title) for tag in tags]

    if request.method == "POST":
        form = QuestionForm(tags_for_ask, request.POST)
        if form.is_valid():
            valid_tag = _behavior.check_match_new_tag(form.cleaned_data.get("new_tags"))
            if not valid_tag:
                form.add_error(field=None, error="This tag's already existed !")
            question = _behavior.create_question(user, **form.cleaned_data)
            return redirect(reverse("question", kwargs={"question_id": question.id}))
    else:
        form = QuestionForm(tags_for_ask)

    tags, members = _behavior.get_tags_and_members()
    return render(request, "ask.html",
                  context={
                      "user": user,
                      "form": form,
                      "tags": tags,
                      "members": members,
                  })


@login_required(login_url="login")
@csrf_protect
def get_settings(request):
    user = _behavior.get_auth_user(request)

    if request.method == "POST":
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            _behavior.update_user_and_profile(user, **form.cleaned_data)
    else:
        form = ProfileEditForm(
            initial={"username": user.username, "email": user.email}
        )
    tags, members = _behavior.get_tags_and_members()
    return render(request, "settings.html",
                  context={
                      "form": form,
                      "user": user,
                      "tags": tags,
                      "members": members,
                  })


def get_member(request, user_id: int):
    user = _behavior.get_auth_user(request)
    return HttpResponse(f"Need user id: {user_id}, auth user: {user.username}")


def get_page(request):
    number = request.GET.get('page')
    pages, questions = _behavior.get_page_and_new_questions(number)
    user = _behavior.get_auth_user(request)
    tags, members = _behavior.get_tags_and_members()
    return render(request, "index.html", {
        "user": user,
        "tags": tags,
        "members": members,
        "questions": questions,
        "pages": pages
    })
