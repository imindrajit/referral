# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral_coupon', '0007_auto_20151126_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupons',
            name='use_limit',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usedcoupons',
            name='used_count',
            field=models.IntegerField(default=0),
        ),
    ]
