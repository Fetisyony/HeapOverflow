from django.core.management.base import BaseCommand
from django.core.cache import cache
from app.models import Profile, Tag


class Command(BaseCommand):
    help = 'Update top users and tags'

    def handle(self, *args, **options):
        popular_tags = Tag.objects.get_popular_n_tags()
        cache.set('popular_tags', popular_tags, 60)

        top_users = Profile.objects.get_top_n_users_by_number_of_answers(10)
        cache.set('top_users', top_users, 60)
