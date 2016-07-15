# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.CharField(default='article not null', max_length=255),
            preserve_default=False,
        ),
    ]
