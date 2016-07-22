# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_article_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friend',
            field=models.ManyToManyField(related_name='friend_rel_+', verbose_name='\u7528\u6237\u670b\u53cb\u5173\u7cfb', to='web.UserProfile', blank=True),
        ),
    ]
