from django.db import models
from django.contrib.auth.models import User


class Manager(models.Manager):
    def get_alive(self):
        return self.filter(died_at__is_null=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField('Genre')  # related_name - how we can access the books from the genre
    created_at = models.DateTimeField(auto_now_add=True)  # when we create newly create an entity
    updated_at = models.DateTimeField(auto_now=True)  # when any changes

    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Book, on_delete=models.CASCADE)  # on_delete=models.CASCADE - if we delete the book, we delete the author
    birthday_at = models.DateField()
    died_at = models.DateField(null=True, blank=True)  # null=True - allow to be empty, blank=True - an empty field can come from the form
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Manager()

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    STATUS_CHOICES = [
        ('a', 'Available'),
        ('na', 'Not Available'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    