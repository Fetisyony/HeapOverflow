import json
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Question, Profile, Tag, Answer
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm, LoginForm, NewQuestionForm, ProfileEditFrom, RegisterForm, UserEditForm
from django.views.decorators.http import require_POST
from cent import Client, PublishRequest
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Question
from django.db.models import F
from django.conf import settings



def search(request):
    query = request.GET.get('q')
    if query:
        search_query = SearchQuery(query)
        search_results = Question.objects.annotate(
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(rank__gte=0.1).order_by('-rank')
    else:
        search_results = Question.objects.none()
    
    page, page_number = paginate(search_results, request, per_page=10)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="search_results.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'query': query,
        }
    )

def search_suggestions(request):
    NUMBER_OF_SUGGESTIONS = 10
    query = request.GET.get('q')
    if query:
        search_results = Question.objects.filter(
            search_vector=query
        )[:NUMBER_OF_SUGGESTIONS]
        suggestions = [{'title': q.title, 'content': q.body[:100], 'id': q.id} for q in search_results]
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)

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

    page, page_number = paginate(questions, request, per_page=10)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="index.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'current_profile': profile,
        }
    )

def hot(request):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    hot_questions = Question.objects.get_hot_questions()

    page, page_number = paginate(hot_questions, request, per_page=10)
    if (page is None):
        return redirect(f"/?page={page_number}")

    return render(
        request,
        template_name="hot.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'current_profile': profile
        }
    )

def tag(request, tag_name):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    questions = Question.objects.get_questions_by_tag_name(tag_name)

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

            'current_profile': profile
        }
    )

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    if (request.method == 'POST'):
        user_form = UserEditForm(request.POST, instance=request.user, user=request.user)
        profile_form = ProfileEditFrom(request.POST, request.FILES, instance=request.user.profile)

        if (user_form.is_valid() and profile_form.is_valid()):
            user_form.save()
            profile_form.save()
            return redirect(reverse("profile_edit"))
        else:
            messages.error(request, 'Invalid data')
    else:
        user_form = UserEditForm(instance=request.user, user=request.user)
        profile_form = ProfileEditFrom(instance=request.user.profile)

    return render(
        request,
        template_name="profile_edit.html",
        context={
            'current_profile': profile,
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )


def render_new_answer(request, answer_id):
    if request.method == 'GET':
        answer = get_object_or_404(Answer, id=answer_id)
        context = {'answer': answer}
        html = render(request, 'layouts/answer_card.html', context).content.decode('utf-8')
        return JsonResponse({'html': html})

def question(request, question_id):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, user=request.user)
    else:
        profile = None

    if (question_id <= 0) or (not Question.objects.filter(id=question_id).exists()):
        return question_not_found(request)

    answers = Answer.objects.get_answers_by_question_id(question_id)

    page, page_number = paginate(answers, request, per_page=7)
    if (page is None):
        return redirect(f"/?page={page_number}")

    if (request.method == 'POST'):
        form = AnswerForm(request.POST)
        if (form.is_valid()):
            new_answer_id = form.save(profile, question_id)

            client = Client(settings.CENTRIFUGO_API_URL, settings.CENTRIFUGO_API_KEY)
            request = PublishRequest(channel=str(question_id), data={"answer": form.cleaned_data['body'], 'answer_id': new_answer_id})
            result = client.publish(request)

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

    return render(
            request,
            'question_not_found.html',
            status=404,
            context={
                'current_profile': profile,
            }
        )

@login_required
def ask_question(request):
    profile = get_object_or_404(Profile, user=request.user)

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
            'form': form,
            'current_profile': profile,
        }
    )

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if (request.method == 'POST'):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request=request)

            user = auth.authenticate(request, **form.cleaned_data)
            if (user):
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
            'form': form,
        }
    )

def login(request):
    redirect_to = request.GET.get('continue', None)
    if (not redirect_to):
        redirect_to = request.GET.get('next', '/')

    if request.user.is_authenticated:
        return redirect(reverse('index'))

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
        messages.error(request, 'You are not the author of the question')

    return JsonResponse({'is_accepted': current_answer.is_accepted})
