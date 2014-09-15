# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sessions', '__first__'),
        ('asset_manager', '0004_auto_20140822_0135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correct', models.BooleanField(default=False)),
                ('choice', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerAnswerSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.ForeignKey(to='sessions.Session')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent', models.ForeignKey(to='mastermind.PlayerAnswerSet')),
                ('response', models.ForeignKey(to='mastermind.Answer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('order', models.PositiveSmallIntegerField()),
                ('background_image', models.ForeignKey(blank=True, to='asset_manager.Image', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='playerresponse',
            name='question',
            field=models.ForeignKey(to='mastermind.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='mastermind.Question'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('background_image', models.ForeignKey(blank=True, to='asset_manager.Image', null=True)),
            ],
            options={
                'verbose_name_plural': b'Quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(to='mastermind.Quiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playeranswerset',
            name='quiz',
            field=models.ForeignKey(to='mastermind.Quiz'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ScoreRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lower_limit', models.PositiveSmallIntegerField()),
                ('upper_limit', models.PositiveSmallIntegerField()),
                ('text', models.CharField(max_length=120)),
                ('quiz', models.ForeignKey(to='mastermind.Quiz')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
