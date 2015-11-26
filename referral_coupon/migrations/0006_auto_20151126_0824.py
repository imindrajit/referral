# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral_coupon', '0005_auto_20151126_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='wallet',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
    ]
