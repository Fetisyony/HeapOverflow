# Generated by Django 5.1.2 on 2024-11-13 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_answer_created_at_question_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='answervote',
            name='created_at',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='questionvote',
            name='created_at',
            field=models.DateTimeField(default=None),
        ),
    ]
