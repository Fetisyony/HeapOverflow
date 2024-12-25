from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from datetime import timedelta
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db.models import Index


class QuestionManager(models.Manager):
    def get_question_by_id(self, question_id):
        return self.get(pk=question_id)

    def get_hot_questions(self):
        return self.annotate(votes_count_tech=Coalesce(Sum('votes__vote_type'), 0)).order_by('-votes_count_tech')

    def get_questions_by_tag_name(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created_at')

class AnswerManager(models.Manager):
    def get_answers_by_question_id(self, question_id):
        return self.filter(question_id=question_id).annotate(votes_count_tech=Coalesce(Sum('votes__vote_type'), 0)).order_by('-is_accepted', 'created_at')

class ProfileManager(models.Manager):
    def get_top_n_users_by_number_of_answers(self, n):
        # это 10 пользователей задавших самые популярные вопросы или давших самые популярные ответы за последнюю неделю
        time_threshold = models.functions.Now() - timedelta(days=7)
        return self.annotate(
            answers_count=models.Count(
                    'answers',
                    filter=models.Q(answers__created_at__gte=time_threshold)
                ) + models.Count(
                    'questions',
                    filter=models.Q(questions__created_at__gte=time_threshold))
                ).order_by('-answers_count')[:n]

class TagManager(models.Manager):
    def get_popular_n_tags(self, n=10):
        time_threshold = models.functions.Now() - timedelta(days=90)
        return self.annotate(
            questions_count=models.Count(
                                            'questions',
                                            filter=models.Q(questions__created_at__gte=time_threshold))
                                        ).order_by('-questions_count')[:n]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, through='QuestionTag', related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    search_vector = SearchVectorField(null=True)

    objects = QuestionManager()

    class Meta:
        indexes = [
            Index(fields=['search_vector'], name='search_vector_idx')
        ]

    def votes_count(self):
        return self.votes.aggregate(votes_count=Sum('vote_type'))['votes_count'] or 0

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AnswerManager()

    def votes_count(self):
        return self.votes.aggregate(votes_count=Sum('vote_type'))['votes_count'] or 0

    def __str__(self):
        return f"Answer to: {self.question.title}"

class QuestionVote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='voted_questions')
    vote_type = models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'user')

    def __str__(self):
        return f"{self.question} - {self.user} - {self.vote_type}"

class AnswerVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='voted_answers')
    vote_type = models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')

    def __str__(self):
        return f"{self.answer} - {self.user} - {self.vote_type}"

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'tag') # to prevent duplicate tags

    def __str__(self):
        return f"({self.question.title} -- {self.tag.name})"
