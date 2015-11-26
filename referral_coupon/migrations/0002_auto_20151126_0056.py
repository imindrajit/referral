# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral_coupon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='referral_code',
            field=models.CharField(max_length=10, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='referred_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='wallet',
            field=models.FloatField(null=True),
        ),
    ]
