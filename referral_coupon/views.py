from django.shortcuts import render_to_response, RequestContext, HttpResponse

def home(request):
    context = RequestContext(request)
    return render_to_response('referral_coupon/home.html', {}, context)

def user(request, id):
    context = RequestContext(request)
    return render_to_response('referral_coupon/user.html', {"id" : id}, context)

def add_user(request):
    context = RequestContext(request)
    return render_to_response('referral_coupon/add_user.html', {} , context)

def generate_referral_code(request):
    context = RequestContext(request)
    return render_to_response('referral_coupon/generate_referral_code.html', {}, context)

def all_users(request):
    context = RequestContext(request)
    return render_to_response('referral_coupon/all_users.html', {}, context)

def generate_coupon(request):
    context = RequestContext(request)
    return render_to_response('referral_coupon/generate_coupon.html', {}, context)

def redeem_coupon(request):
    context = RequestContext(request)
    return render_to_response('referral_coupon/redeem_coupon.html', {}, context)