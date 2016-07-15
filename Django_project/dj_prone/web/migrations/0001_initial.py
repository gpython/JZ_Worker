# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('gender', models.BooleanField(default=False)),
                ('age', models.IntegerField(default=19)),
                ('memo', models.TextField(default=b'xxxx')),
                ('createtime', models.DateTimeField(default=b'2016-06-06 06:06:06')),
                ('group_relation', models.ManyToManyField(to='web.Group')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='typeId',
            field=models.ForeignKey(to='web.UserType'),
        ),
    ]
