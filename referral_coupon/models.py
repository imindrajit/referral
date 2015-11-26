from django.db import models
from django.utils.crypto import get_random_string
from referral.settings import LIMIT
import datetime

# Create your models here.
class Users(models.Model):
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False)
    referral_code = models.CharField(null=True, blank=True, max_length=100, unique=True)
    referred_by = models.IntegerField(blank=True, null=True)
    referred_by_code = models.CharField(null=True, blank=True, max_length=10)
    referral_score = models.IntegerField(default=0)
    wallet = models.FloatField(null=True, blank=True, default=0.00)

    def as_json(self):
        return dict(
            id=self.pk,
            name=self.name,
            email=self.email,
            referral_code=self.referral_code,
            referred_by=self.referred_by,
            referral_by_code=self.referred_by_code,
            referral_score=self.referral_score,
            wallet=self.wallet)

    def generate_referral_code(self):
        if self.referral_code is not None:
            print "code already hai"
            return
        else:
            code = get_random_string(length=5)
            self.referral_code = str(self.pk) + code
            self.save()

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']



class Coupons(models.Model):
    coupon_code = models.CharField(blank=False, null=False, max_length=100)
    value = models.IntegerField(blank=False, null=False, default=100)
    use_limit = models.IntegerField(blank=False, null=False, default=0)

    def as_json(self):
        return dict(
            id=self.pk,
            coupon_code=self.coupon_code,
            value=self.value,
            use_limit=self.use_limit)

    def generate_coupon_code(self, val, use_limit):
        code = get_random_string(length=4)
        self.coupon_code = code + str(val)
        self.value = val
        self.use_limit = use_limit
        self.save()

    def __unicode__(self):
        return '%s' % (self.coupon_code)

    class Meta:
        ordering = ['-value']


class UsedCoupons(models.Model):
    user = models.ForeignKey(Users)
    coupon = models.ForeignKey(Coupons)
    used_count = models.IntegerField(blank=False, null=False, default=0)

    def as_json(self):
        return dict(
            id=self.pk,
            coupon=self.coupon,
            used_count=self.used_count
        )

    def __unicode__(self):
        return '%s' % (self.user)

    class Meta:
        ordering = ['-used_count']