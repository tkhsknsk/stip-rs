# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2019-03-01 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctirs', '0018_auto_20190220_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='locale',
            field=models.CharField(choices=[(b'en', 'English'), (b'pt-br', 'Portuguese'), (b'es', 'Spanish'), (b'ja', 'Japanese'), (b'fr', 'French'), (b'zh-cn', 'Chinese')], default='en', max_length=4),
        ),
    ]
