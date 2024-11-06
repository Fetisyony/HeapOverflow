from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from app.data import QUESTIONS, USERS_DATABASE, TOP_USER_ID, POPULAR_TAGS


def index(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 4)
    page = paginator.page(page_number)

    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="index.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def hot(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_number)

    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="hot.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def settings(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="settings.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def question(request, question_id):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="question.html",
        context={
            'question': QUESTIONS[question_id],
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def askQuestion(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="ask.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def tag(request, tag_name):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_number)

    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="tag.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'tag_name': tag_name,

            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def register(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="register.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def login(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="login.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )
