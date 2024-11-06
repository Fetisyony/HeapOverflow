from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from random import sample, choice

POPULAR_TAGS = ["python", "ruby", "linux", "kotlin", "arch", "c++", "android", "ios", "django", "flask"]
tags = POPULAR_TAGS + ["fastapi", "sql", "nosql", "postgresql", "mysql", "sqlite"]

USERS_DATABASE = [
    {
        "name" : "Ryan Gosling",
        "avatar" : "img/AnswerProfile1.jpg",
    },
    {
        "name" : "Oscar Isaac",
        "avatar" : "img/AnswerProfile2.png",
    },
    {
        "name" : "Peter",
        "avatar" : "img/AnswerProfile3.png",
    },
    {
        "name" : "Carrey Mulligan",
        "avatar" : "{% static img/Avatar.jpg %}",
    },
    {
        "name" : "Christina Hendricks",
        "avatar" : "img/AnswerProfile2.png",
    }
]

QUESTIONS = [
    {
        'title': 'title ' + str(i),
        'id': i,
        'text': 'This is text of the question' + str(i),
        'tags': sample(tags, 3),
        'author': choice(USERS_DATABASE),
    } for i in range(30)
]

POPULAR_TAGS = ["python", "ruby", "linux", "kotlin", "arch", "c++", "android", "ios"]
TOP_USER_ID = [0, 1, 2]

tags = []

def index(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
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

def profile(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="profile.html",
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
