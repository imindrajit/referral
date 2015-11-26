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