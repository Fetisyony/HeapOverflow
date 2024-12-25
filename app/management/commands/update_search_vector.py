from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from app.models import Question
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Update search_vector field for existing questions'

    def handle(self, *args, **kwargs):
        questions = Question.objects.all()
        for question in tqdm(questions, desc='Updating search_vector for all questions'):
            question.search_vector = (
                SearchVector('title', weight='A') +
                SearchVector('body', weight='B')
            )
            question.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated search_vector for all questions'))
