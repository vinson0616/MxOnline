# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-22 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170922_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[(b'register', b'\xe6\xb3\xa8\xe5\x86\x8c'), (b'forget', b'\xe6\x89\xbe\xe5\x9b\x9e\xe5\xaf\x86\xe7\xa0\x81'), (b'update_email', '\u4fee\u6539\u90ae\u7bb1')], max_length=20, verbose_name=b'\xe9\xaa\x8c\xe8\xaf\x81\xe7\xa0\x81\xe7\xb1\xbb\xe5\x9e\x8b'),
        ),
    ]
