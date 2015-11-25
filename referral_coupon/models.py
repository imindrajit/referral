from django.db import models
import datetime

# Create your models here.
class Users(models.Model):
    name = models.CharField(blank=False, max_length=50)
    email = models.EmailField(blank=False)
    referral_code = models.CharField(blank=True, max_length=10, unique=True)
    referred_by = models.IntegerField(blank=True)
    referral_score = models.IntegerField(default=0)
    wallet = models.FloatField(blank=True)

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']



class Coupons(models.Model):
    coupon_code = models.CharField(blank=False, max_length=10)
    valid_till = models.DateField()

    class Meta:
        ordering = ['-valid_till']



class UsedCoupons(models.Model):
    user = models.ForeignKey(Users)
    coupon = models.ForeignKey(Coupons)