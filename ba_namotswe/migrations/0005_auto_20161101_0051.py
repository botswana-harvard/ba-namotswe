# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-01 00:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ba_namotswe', '0004_auto_20161101_0047'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='labtest',
            unique_together=set([('lab_record', 'utest_id', 'test_date')]),
        ),
    ]
