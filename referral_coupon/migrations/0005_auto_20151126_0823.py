# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral_coupon', '0004_users_referred_by_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='wallet',
            field=models.FloatField(default=0.0),
        ),
    ]
