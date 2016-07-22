# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_userprofile_friend'),
    ]

    operations = [
        migrations.CreateModel(
            name='CGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u7fa4\u7ec4\u540d\u5b57')),
                ('brief', models.TextField(default=b'Nothing', max_length=1024, verbose_name='\u7b80\u4ecb')),
                ('member_limit', models.IntegerField(default=200L, verbose_name='\u4eba\u5458\u9650\u5236')),
                ('admin', models.ManyToManyField(related_name='group_admin', verbose_name='\u7ba1\u7406\u5458', to='web.UserProfile')),
                ('founder', models.ForeignKey(verbose_name='\u521b\u59cb\u4eba', to='web.UserProfile')),
                ('member', models.ManyToManyField(related_name='group_member', verbose_name='\u7ec4\u5458', to='web.UserProfile')),
            ],
        ),
    ]
