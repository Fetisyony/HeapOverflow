from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app.data import QUESTIONS, POPULAR_TAGS, TOP_USER_LIST


def paginate(objects_list, request, per_page=4):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)

    if page_number < 1:
        page_number = 1
        return None, page_number
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages
        return None, page_number

    page = paginator.get_page(page_number)
    return page, page_number

def index(request):
    page, page_number = paginate(QUESTIONS, request, per_page=4)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="index.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def hot(request):
    page, page_number = paginate(QUESTIONS, request, per_page=4)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="hot.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def settings(request):
    return render(
        request,
        template_name="settings.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def question(request, question_id):
    if (question_id < 0) or (question_id >= len(QUESTIONS)):
        return render(
                        request, 
                        'question_not_found.html',
                        status=404,
                        context={
                            'popular_tags': POPULAR_TAGS,
                            'top_users': TOP_USER_LIST
                        }
                    )

    return render(
        request,
        template_name="question.html",
        context={
            'question': QUESTIONS[question_id],
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def wrong_url(request, wrong_url):
    return render(
        request,
        template_name="wrong_url.html",
        status=404,
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def ask_question(request):
    return render(
        request,
        template_name="ask.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def tag(request, tag_name):
    page, page_number = paginate(QUESTIONS, request, per_page=4)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="tag.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'tag_name': tag_name,

            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def register(request):
    return render(
        request,
        template_name="register.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )

def login(request):
    return render(
        request,
        template_name="login.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USER_LIST
        }
    )
