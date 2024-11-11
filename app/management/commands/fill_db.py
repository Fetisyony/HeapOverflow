import random
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from django.db import transaction
from app.models import Question, Answer, QuestionLike, AnswerLike, Tag, QuestionTag, Profile, Profile
from faker import Faker
from tqdm import tqdm
import os

fake = Faker()

DEFAULT_POPULATION_VALUE = 10

PROFILE_IMG_PATH = os.path.join(settings.MEDIA_ROOT, 'images')


class Command(BaseCommand):
    help = 'Populates the database with sample data.'
    population_value_arg_name = 'ratio'

    tags_per_question_number = 3

    batch_size = 1000

    def add_arguments(self, parser):
        parser.add_argument(self.population_value_arg_name, nargs='?', type=int,
                            default=DEFAULT_POPULATION_VALUE, help='Number of users to create')

    def init_values(self, population_value):
        self.population_value = population_value
        self.user_number = population_value
        self.question_number = population_value * 10
        self.answer_number = population_value * 100
        self.tag_number = population_value
        self.like_number = population_value * 200

    def handle(self, *args, **options):
        self.init_values(options[self.population_value_arg_name])

        self.generate_users()
        self.generate_questions()
        self.generate_answers()
        self.generate_tags()
        self.generate_question_likes()
        self.generate_answer_likes()

    def generate_users(self):
        import os

        images = os.listdir(PROFILE_IMG_PATH)

        user_batch = []
        profile_batch = []

        for i in tqdm(range(self.user_number), desc="Creating Users and Profiles"):
            user = User(username=fake.user_name(), password='1')
            user.save()
            user_batch.append(user)

            random_image = random.choice(images)

            profile = Profile(user=user)
            with open(os.path.join(PROFILE_IMG_PATH, random_image), 'rb') as img_file:
                profile.profile_picture.save(random_image, File(img_file))

            profile.save()
            profile_batch.append(profile)

        with transaction.atomic():
            for user in user_batch:
                user.save()

            for profile in profile_batch:
                profile.save()

    def generate_questions(self):
        question_batch = []

        profile_ids = Profile.objects.values_list('id', flat=True)

        for i in tqdm(range(self.question_number), desc="Creating Questions"):
            question = Question(
                user_id=random.choice(profile_ids),
                title=fake.sentence(),
                body=fake.text(),
            )
            question_batch.append(question)

            if (i + 1) % self.batch_size == 0:
                Question.objects.bulk_create(question_batch)
                question_batch = []

        if len(question_batch):
            Question.objects.bulk_create(question_batch)

    def generate_answers(self):
        answer_batch = []

        profile_ids = Profile.objects.values_list('id', flat=True)
        question_ids = Question.objects.values_list('id', flat=True)

        for i in tqdm(range(self.answer_number), desc="Creating Answers"):
            answer = Answer(
                user_id=random.choice(profile_ids),
                question_id=random.choice(question_ids),
                body=fake.paragraph(),
            )
            answer_batch.append(answer)

            if (i + 1) % self.batch_size == 0:
                Answer.objects.bulk_create(answer_batch)
                answer_batch = []

        if len(answer_batch):
            Answer.objects.bulk_create(answer_batch)
        
    def generate_question_likes(self):
        question_like_batch = []

        users = list(Profile.objects.all())

        used_questions = {}
        question_ids = Question.objects.values_list('id', flat=True)
        profile_ids = Profile.objects.values_list('id', flat=True)

        for _ in tqdm(range(self.like_number), desc="Creating Likes"):
            question_like = QuestionLike(
                question_id=random.choice(question_ids),
                user_id=random.choice(profile_ids),
            )
            if (question_like.user_id not in used_questions):
                used_questions[question_like.user_id] = {question_like.question_id}
            else:
                while question_like.question_id in used_questions[question_like.user_id]:
                    question_like.question_id = random.choice(question_ids)
                used_questions[question_like.user_id].add(question_like.question_id)
            question_like_batch.append(question_like)

        QuestionLike.objects.bulk_create(question_like_batch)
    
    def generate_answer_likes(self):
        answer_like_batch = []

        users = list(Profile.objects.all())

        used_answers = {}
        answers_ids = Answer.objects.values_list('id', flat=True)
        profile_ids = Profile.objects.values_list('id', flat=True)

        for i in tqdm(range(self.like_number), desc="Creating Likes"):
            answer_like = AnswerLike(
                answer_id=random.choice(answers_ids),
                user_id=random.choice(profile_ids),
            )
            if (answer_like.user_id not in used_answers):
                used_answers[answer_like.user_id] = {answer_like.answer_id}
            else:
                while answer_like.answer_id in used_answers[answer_like.user_id]:
                    answer_like.answer_id = random.choice(answers_ids)
                used_answers[answer_like.user_id].add(answer_like.answer_id)
            answer_like_batch.append(answer_like)
        
        AnswerLike.objects.bulk_create(answer_like_batch)

    def generate_tags(self):
        pull_of_tags = set(["python", "windows", "shell", "ruby", "testing", "django", "flask", "sql", "nosql", "docker", "kubernetes", "aws", "azure", "gcp", "devops", "git", "github", "gitlab", "bitbucket", "javascript", "typescript", "react", "angular", "vue", "nodejs", "express", "mongodb", "postgresql", "mysql", "sqlite", "redis", "rabbitmq", "kafka", "nginx", "apache", "gunicorn", "uwsgi", "jinja", "html", "css", "sass", "less", "bootstrap", "tailwind", "webpack", "gulp", "grunt", "babel", "eslint", "prettier", "jest", "mocha", "chai", "cypress", "selenium", "webdriver", "appium", "jenkins", "circleci", "bitbucket-pipelines", "heroku", "netlify", "vercel", "digitalocean", "linode", "aws-lambda", "azure-functions", "google-cloud-functions", "serverless", "nextjs", "nuxtjs", "deno", "nestjs", "wordpress", "joomla", "api", "magento", "shopify", "woocommerce", "prestashop", "opencart", "bigcommerce", "salesforce", "sap", "oracle", "microsoft", "android", "ios", "flutter", "react-native", "ionic", "cordova", "phonegap", "xamarin", "unity", "unreal", "godot", "blender", "maya", "3ds-max", "autocad", "solidworks"])

        tags = []
        for tag_name in tqdm(pull_of_tags, desc="Creating Tags"):
            tags.append(Tag(name=tag_name))

        Tag.objects.bulk_create(tags)

        question_tags = []
        for question in tqdm(Question.objects.all(), desc="Assigning Tags to Questions"):
            num_tags = random.randint(2, self.tags_per_question_number)
            question_tags.extend([QuestionTag(question=question, tag=tag) for tag in random.sample(tags, num_tags)])

        QuestionTag.objects.bulk_create(question_tags)
