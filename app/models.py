from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def get_question_by_id(self, question_id):
        return self.get(pk=question_id)

    def get_hot_questions(self):
        return self.annotate(likes_count=models.Count('likes')).order_by('-likes_count')

    def get_questions_by_tag_name(self, tag_name):
        return self.filter(tags__name=tag_name)

class AnswerManager(models.Manager):
    def get_answers_by_question_id(self, question_id):
        return self.filter(question_id=question_id).annotate(likes_count=models.Count('likes')).order_by('-is_accepted', '-likes_count')

class ProfileManager(models.Manager):
    def get_top_n_users_by_number_of_answers(self, n):
        return self.annotate(answers_count=models.Count('answers')).order_by('-answers_count')[:n]

class TagManager(models.Manager):
    def get_popular_n_tags(self, n=5):
        return self.annotate(questions_count=models.Count('questions')).order_by('-questions_count')[:n]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

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

    objects = QuestionManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer to: {self.question.title}"

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='liked_questions')

    class Meta:
        unique_together = ('question', 'user')

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='liked_answers')

    class Meta:
        unique_together = ('answer', 'user')
    
    def __str__(self):
        return f"{self.answer} - {self.user}"

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'tag') # to prevent duplicate tags
    
    def __str__(self):
        return f"({self.question.title} -- {self.tag.name})"
