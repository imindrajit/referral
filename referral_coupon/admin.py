from django.contrib import admin
from referral_coupon.models import Users, Coupons, UsedCoupons

admin.site.register(Users)
admin.site.register(Coupons)
admin.site.register(UsedCoupons)
