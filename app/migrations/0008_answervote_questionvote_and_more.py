# Generated by Django 5.1.2 on 2024-11-12 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_question_tags_alter_questiontag_question_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])),
            ],
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='answerlike',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='answerlike',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='answerlike',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='questionlike',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='questionlike',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionlike',
            name='user',
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(condition=models.Q(('name__iexact', None)), fields=('name',), name='unique_tag_name_case_insensitive'),
        ),
        migrations.AddField(
            model_name='answervote',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='app.answer'),
        ),
        migrations.AddField(
            model_name='answervote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted_answers', to='app.profile'),
        ),
        migrations.AddField(
            model_name='questionvote',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='app.question'),
        ),
        migrations.AddField(
            model_name='questionvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted_questions', to='app.profile'),
        ),
        migrations.DeleteModel(
            name='AnswerLike',
        ),
        migrations.DeleteModel(
            name='QuestionLike',
        ),
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together={('answer', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='questionvote',
            unique_together={('question', 'user')},
        ),
    ]
