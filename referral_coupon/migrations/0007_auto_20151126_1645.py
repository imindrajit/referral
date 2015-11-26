# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral_coupon', '0006_auto_20151126_0824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupons',
            options={'ordering': ['-value']},
        ),
        migrations.AlterModelOptions(
            name='usedcoupons',
            options={'ordering': ['-used_count']},
        ),
        migrations.RemoveField(
            model_name='coupons',
            name='valid_till',
        ),
        migrations.AddField(
            model_name='coupons',
            name='value',
            field=models.IntegerField(default=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usedcoupons',
            name='used_count',
            field=models.IntegerField(default=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coupons',
            name='coupon_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='users',
            name='referral_code',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
    ]
