# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral_coupon', '0002_auto_20151126_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='coupon_code',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='referral_code',
            field=models.CharField(max_length=10, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='referred_by',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='wallet',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
