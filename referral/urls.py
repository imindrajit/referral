from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from referral_coupon import views
from api import apis
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', views.home, name='home'),
    url(r'^add-user/$', views.add_user, name='add_user'),
    url(r'^user/(?P<id>\d+)/?$', views.user, name='user'),
    url(r'^all-users/$', views.all_users, name='all_users'),
    url(r'^generate-referral-code/$', views.generate_referral_code, name='generate_referral_code'),
    url(r'^generate-coupon/$', views.generate_coupon, name='generate_coupon'),
    url(r'^redeem-coupon/$', views.redeem_coupon, name='redeem_coupon'),
    url(r'^api/v1/user/$', apis.user, name='user'),
    url(r'^api/v1/user/(?P<id>\d+)/?$', apis.get_user, name='get_user'),
    url(r'^api/v1/users/$', apis.all_users, name='all_users'),
    url(r'^api/v1/user/generate-referral-code/$', apis.generate_referral_code, name='generate_referral_code'),
    url(r'^api/v1/user/generate-coupon-code/$', apis.generate_coupon_code, name='generate_coupon_code'),
    url(r'^api/v1/user/redeem-code/$', apis.redeem_code, name='redeem_code'),
    url(r'^api/v1/check-email/$', apis.check_email, name='check_email'),
    url(r'^api/v1/check-referral-code/$', apis.check_referral_code, name='check_referral_code')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
