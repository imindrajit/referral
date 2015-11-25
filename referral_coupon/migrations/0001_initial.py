# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coupon_code', models.CharField(max_length=10)),
                ('valid_till', models.DateField()),
            ],
            options={
                'ordering': ['-valid_till'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsedCoupons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coupon', models.ForeignKey(to='referral_coupon.Coupons')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75)),
                ('referral_code', models.CharField(unique=True, max_length=10, blank=True)),
                ('referred_by', models.IntegerField(blank=True)),
                ('referral_score', models.IntegerField(default=0)),
                ('wallet', models.FloatField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='usedcoupons',
            name='user',
            field=models.ForeignKey(to='referral_coupon.Users'),
            preserve_default=True,
        ),
    ]
