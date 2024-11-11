from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import Question, Profile, Tag, QuestionTag, Answer, QuestionLike, AnswerLike


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
    questions = Question.objects.all()
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    page, page_number = paginate(questions, request, per_page=10)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="index.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )

def hot(request):
    hot_questions = Question.objects.get_hot_questions()
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    page, page_number = paginate(hot_questions, request, per_page=4)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="hot.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )

def settings(request):
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    return render(
        request,
        template_name="settings.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )

def question(request, question_id):
    questions = Question.objects.get_hot_questions()
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    if (question_id < 0) or (question_id >= len(questions)):
        return render(
                        request, 
                        'question_not_found.html',
                        status=404,
                        context={
                            'popular_tags': popular_tags,
                            'top_users': top_users
                        }
                    )

    return render(
        request,
        template_name="question.html",
        context={
            'question': Question.objects.get_question_by_id(question_id),
            'answers': Answer.objects.get_answers_by_question_id(question_id),
            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )

def ask_question(request):
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    return render(
        request,
        template_name="ask.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )

def tag(request, tag_name):
    questions = Question.objects.get_questions_by_tag_name(tag_name)
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    page, page_number = paginate(questions, request, per_page=4)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="tag.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'tag_name': tag_name,

            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )

def register(request):
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    return render(
        request,
        template_name="register.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )

def login(request):
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    return render(
        request,
        template_name="login.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users
        }
    )
