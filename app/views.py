import json
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Question, Profile, Tag, Answer
from django.db.models import Sum
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm, LoginForm, NewQuestionForm, ProfileEditFrom, RegisterForm, UserEditForm
from django.views.decorators.csrf import csrf_protect as ccrf_protect
from django.utils import timezone
from askme_fetisov.settings import MEDIA_URL
from django.views.decorators.http import require_POST
import os
import jwt
import time


def paginate(objects_list, request, per_page=8):
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
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    questions = Question.objects.order_by('-created_at')

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
            'top_users': top_users,
            'current_profile': profile,
        }
    )

def hot(request):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    hot_questions = Question.objects.get_hot_questions()
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    page, page_number = paginate(hot_questions, request, per_page=10)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="hot.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': popular_tags,
            'top_users': top_users,
            'current_profile': profile
        }
    )

def tag(request, tag_name):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    questions = Question.objects.get_questions_by_tag_name(tag_name)
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    page, page_number = paginate(questions, request, per_page=10)
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
            'top_users': top_users,
            'current_profile': profile
        }
    )

@login_required
def settings(request):
    profile = get_object_or_404(Profile, user=request.user)
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    if (request.method == 'POST'):
        user_form = UserEditForm(request.POST, instance=request.user, user=request.user)
        profile_form = ProfileEditFrom(request.POST, request.FILES, instance=request.user.profile)

        if (user_form.is_valid() and profile_form.is_valid()):
            user_form.save()
            profile_form.save()
            return redirect(reverse("settings"))
        else:
            print("error")
            print(user_form["username"].errors)
    else:
        user_form = UserEditForm(instance=request.user, user=request.user)
        profile_form = ProfileEditFrom(instance=request.user.profile)

    return render(
        request,
        template_name="settings.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users,
            'current_profile': profile,
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )

def question(request, question_id):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    if (question_id <= 0) or (not Question.objects.filter(id=question_id).exists()):
        return question_not_found(request)

    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    answers = Answer.objects.get_answers_by_question_id(question_id)

    page, page_number = paginate(answers, request, per_page=7)
    if (page is None):
        return redirect(f"/?page={page_number}")

    if (request.method == 'POST'):
        form = AnswerForm(request.POST)
        if (form.is_valid()):
            new_answer_id = form.save(profile, question_id)
            page_number = (Answer.objects.filter(question_id=question_id).count() + 7-1 ) //7
            return redirect(reverse('question', args=[question_id]) + f"?page={page_number}#answer-{new_answer_id}")

        if (not question_id):
            messages.error(request, 'Question not found')
            return redirect(reverse('index'))
    else:
        form = AnswerForm

    current_user_is_author = False
    if (profile):
        current_user_is_author = Question.objects.get_question_by_id(question_id).user == profile

    return render(
        request,
        template_name="question.html",
        context={
            'question': Question.objects
                .get_question_by_id(question_id),
            'page_obj': page,
            'popular_tags': popular_tags,
            'top_users': top_users,
            'current_profile': profile,
            'form': form,
            'is_author': current_user_is_author,
        }
    )

def question_not_found(request):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    return render(
            request,
            'question_not_found.html',
            status=404,
            context={
                'popular_tags': popular_tags,
                'top_users': top_users,
                'current_profile': profile,
            }
        )

@login_required
def ask_question(request):
    profile = get_object_or_404(Profile, user=request.user)
    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    if (request.method == 'POST'):
        form = NewQuestionForm(request.POST)
        if (form.is_valid()):
            new_question_id = form.save(profile)
            return redirect(reverse('question', args=[new_question_id]))
    else:
        form = NewQuestionForm()

    return render(
        request,
        template_name="ask.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users,
            'form': form,
            'current_profile': profile,
        }
    )

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    if (request.method == 'POST'):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request=request)

            user = auth.authenticate(request, **form.cleaned_data)
            if (user):
                print("Logging in...")
                auth.login(request, user)
                request.session.set_expiry(1209600)
            else:
                form.add_error(None, 'Invalid username or password')
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(
        request,
        template_name="register.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users,
            'form': form,
        }
    )

def login(request):
    redirect_to = request.GET.get('continue', None)
    if (not redirect_to):
        redirect_to = request.GET.get('next', '/')

    if request.user.is_authenticated:
        return redirect(reverse('index'))

    popular_tags = Tag.objects.get_popular_n_tags()
    top_users = Profile.objects.get_top_n_users_by_number_of_answers(5)

    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        redirect_to = request.POST.get('continue')
        if (form.is_valid()):
            user = auth.authenticate(request, **form.cleaned_data)
            if (user):
                auth.login(request, user)
                if (form.cleaned_data['remember']):
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                return redirect(redirect_to)
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(
        request,
        template_name="login.html",
        context={
            'popular_tags': popular_tags,
            'top_users': top_users,
            'form': form,
            'continue': redirect_to,
        }
    )

def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

@require_POST
@login_required
def vote_answer(request, answer_id):
    body = json.loads(request.body)
    vote_type = 1 if body.get('type') == 'Like' else -1
    opposite_vote_type = -vote_type

    profile = get_object_or_404(Profile, user=request.user)
    current_answer = Answer.objects.get(id=answer_id)

    if (current_answer.votes.filter(user=profile, vote_type=vote_type).exists()):
        current_answer.votes.filter(user=profile, vote_type=vote_type).delete()
    else:
        if (current_answer.votes.filter(user=profile, vote_type=opposite_vote_type).exists()):
            current_answer.votes.filter(user=profile, vote_type=opposite_vote_type).delete()
        current_answer.votes.create(user=profile, vote_type=vote_type)

    vote_count = current_answer.votes_count()
    return JsonResponse({'vote_count': vote_count})

@require_POST
@login_required
def vote_question(request, question_id):
    body = json.loads(request.body)
    vote_type = 1 if body.get('type') == 'Like' else -1
    opposite_vote_type = -vote_type

    profile = get_object_or_404(Profile, user=request.user)
    current_question = Question.objects.get(id=question_id)

    if (current_question.votes.filter(user=profile, vote_type=vote_type).exists()):
        current_question.votes.filter(user=profile, vote_type=vote_type).delete()
    else:
        if (current_question.votes.filter(user=profile, vote_type=opposite_vote_type).exists()):
            current_question.votes.filter(user=profile, vote_type=opposite_vote_type).delete()
        current_question.votes.create(user=profile, vote_type=vote_type)

    vote_count = current_question.votes_count()
    return JsonResponse({'vote_count': vote_count})

@login_required
@require_POST
def tick_correct(request, answer_id):
    current_answer = get_object_or_404(Answer, id=answer_id)
    current_question = current_answer.question

    if (current_question.user == request.user.profile):
        if (current_answer.is_accepted):
            current_answer.is_accepted = False
        else:
            current_answer.is_accepted = True
        current_answer.save()
    else:
        print("Not authorized")

    return JsonResponse({'is_accepted': current_answer.is_accepted})
