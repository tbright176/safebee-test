# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0014_auto_20140910_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playeranswerset',
            name='quiz',
            field=models.ForeignKey(related_name=b'+', to='mastermind.Quiz'),
        ),
        migrations.AlterField(
            model_name='playerresponse',
            name='question',
            field=models.ForeignKey(related_name=b'+', to='mastermind.Question'),
        ),
        migrations.AlterField(
            model_name='playerresponse',
            name='response',
            field=models.ForeignKey(related_name=b'+', to='mastermind.Answer'),
        ),
        migrations.AlterField(
            model_name='question',
            name='background_image',
            field=models.ForeignKey(related_name=b'+', blank=True, to='asset_manager.Image', null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='primary_image',
            field=models.ForeignKey(related_name=b'mastermind_quiz_primary_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='promo_image',
            field=models.ForeignKey(related_name=b'mastermind_quiz_promo_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='results_image',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='secondary_author',
            field=models.ForeignKey(related_name=b'+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='social_image',
            field=models.ForeignKey(related_name=b'mastermind_quiz_social_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='quiz',
            field=models.ForeignKey(related_name=b'questions', to='mastermind.Quiz'),
        ),
    ]
