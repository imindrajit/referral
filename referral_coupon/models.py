from django.db import models
from django.utils.crypto import get_random_string
import datetime

# Create your models here.
class Users(models.Model):
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False)
    referral_code = models.CharField(null=True, blank=True, max_length=10, unique=True)
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
    coupon_code = models.CharField(blank=True, null=False, max_length=10)
    valid_till = models.DateField()

    def as_json(self):
        return dict(
            id=self.pk,
            coupon_code=self.coupon_code,
            valid_till = self.valid_till.isoformat())

    class Meta:
        ordering = ['-valid_till']



class UsedCoupons(models.Model):
    user = models.ForeignKey(Users)
    coupon = models.ForeignKey(Coupons)