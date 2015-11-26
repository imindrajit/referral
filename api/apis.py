from django.shortcuts import render_to_response, RequestContext, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import re
import urllib2
from referral.settings import DOMAIN
from referral_coupon.models import Users, Coupons, UsedCoupons

def verify_name(name):
    if len(name) > 50:
        return False
    if re.match("^[A-Za-z ]*$", name):
        return True
    else:
        return False

def verify_email(mail):
    if re.match("[\w\.\-]*@[\w\.\-]*\.\w+", str(mail)):
        url = DOMAIN+'/api/v1/check-email/'
        print url
        req = urllib2.Request(url)
        print req
        try:
            response = urllib2.urlopen(req, json.dumps({'email': mail}))
            return True
        except:
            return False
    else:
        return False

def verify_referral_code(code):
    url = DOMAIN+'/api/v1/check-referral-code/'
    print url
    req = urllib2.Request(url)
    response=None
    try:
        response = urllib2.urlopen(req, json.dumps({'referral_code': code}))
    except:
        print "GALAT REF"
        return "None"
    # print "inside verify func"
    # print response.read()
    return response.read()

def increment_referral_scores(new_user):
    new_user.referral_score = new_user.referral_score + 1
    new_user.save()
    if new_user.referred_by is None:
        return
    parent_user = Users.objects.get(pk=new_user.referred_by)
    increment_referral_scores(parent_user)


@csrf_exempt
def user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print json.dumps(body)
        response = {}
        if body["name"].strip() == "" or body["email"].strip() == "":
            response["message"] = "Please enter valid name and email"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        if verify_name(body["name"]) == False:
            response["message"] = "Please enter a valid name"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        if verify_email(body["email"]) == False:
            response["message"] = "Please enter a valid email or email already registered"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        print "naam pata done"
        referred_by_user = None
        referred_by_user_referral_code = body["referred_by_code"]
        if referred_by_user_referral_code.strip() != "":
            referred_by_user = verify_referral_code(referred_by_user_referral_code)
            if referred_by_user == "None":
                print "coupon wala nahi mila"
                response["message"] = "Please enter a valid referral code"
                return HttpResponse(json.dumps(response), content_type='application/json', status=400)

            referred_by_user = json.loads(referred_by_user)
            print "API return call"
            print referred_by_user
            referred_by_user = referred_by_user["user"]
            print referred_by_user
            print "coupon wala mila"
        else:
            pass

        new_user = Users()
        new_user.name = body["name"]
        new_user.email = body["email"]
        if referred_by_user:
            new_user.referred_by = int(referred_by_user["id"])
            new_user.referred_by_code = referred_by_user["referral_code"]
        new_user.save()
        if referred_by_user:
            increment_referral_scores(new_user)
        response['message'] = "User successfully added"
        response['user'] = new_user.as_json()
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = {}
        try:
            users = Users.objects.get(email=str(body["email"]))
            response["message"] = "Email address already present."
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        except:
            response["message"] = "New Email."
            return HttpResponse(json.dumps(response), content_type='application/json', status=200)

@csrf_exempt
def generate_referral_code(request):
    if request.method == 'POST':
        print "code banao"
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print body
        response = {}
        try:
            curr_user = Users.objects.get(email=str(body["email"]))
            print "yahi wala user hai"
            print curr_user.as_json()
            curr_user.generate_referral_code()
            response["message"] = "Referral Code generated"
            response["user"] = curr_user.as_json()
            return HttpResponse(json.dumps(response), content_type='application/json', status=200)
        except:
            response["message"] = "Enter valid email address"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

@csrf_exempt
def generate_coupon_code(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print body
        response = {}
        try:
            val = body["value"].isdigit()
            use_limit = body["use_limit"].isdigit()
            if val and use_limit and int(body["use_limit"]) > 0:
                curr_coupon = Coupons()
                curr_coupon.generate_coupon_code(int(body["value"]), int(body["use_limit"]))
                response["message"] = "Coupon Code generated"
                response["coupon"] = curr_coupon.as_json()
                return HttpResponse(json.dumps(response), content_type='application/json', status=200)
            else:
                response["message"] = "Enter valid coupon value or coupon use limit"
                return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        except:
            response["message"] = "Enter valid coupon value or coupon use limit"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

def add_money_to_wallet(curr_user, coupon):
    curr_user.wallet = curr_user.wallet + coupon.value
    curr_user.save()
    return

@csrf_exempt
def redeem_code(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print body
        response = {}
        try:
            curr_user = Users.objects.get(email=str(body["email"]))
            # print curr_user.as_json()
            coupon = Coupons.objects.get(coupon_code=str(body["code"]))
            # print coupon.as_json()
            try:
                curr_used_coupon = UsedCoupons.objects.get(user=curr_user, coupon=coupon)
                print "curr used coupon"
                print curr_used_coupon
                print "ye banda pehle coupon use kiya hai"
                if curr_used_coupon.used_count == 0:
                    response["message"] = "Coupon usage limit exceeded"
                    return HttpResponse(json.dumps(response), content_type='application/json', status=400)
                else:
                    curr_used_coupon.used_count = curr_used_coupon.used_count - 1
                    curr_used_coupon.save()
                    add_money_to_wallet(curr_user, coupon)
                    response["message"] = "Coupon amount added to wallet"
                    return HttpResponse(json.dumps(response), content_type='application/json', status=200)
            except:
                print "naya banda hai"
                curr_used_coupon = UsedCoupons()
                curr_used_coupon.user = curr_user
                curr_used_coupon.coupon = coupon
                curr_used_coupon.used_count = coupon.use_limit - 1
                curr_used_coupon.save()
                add_money_to_wallet(curr_user, coupon)
                response["message"] = "Coupon amount added to wallet"
                return HttpResponse(json.dumps(response), content_type='application/json', status=200)
        except:
            response["message"] = "Enter valid email address or coupon code"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)


@csrf_exempt
def check_referral_code(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print "REFERRAL CODE"
        print body["referral_code"]
        response = {}
        try:
            referred_user = Users.objects.get(referral_code=str(body["referral_code"]))
            print "MIL GYA"
            response["message"] = "Valid referral code"
            response["user"] = referred_user.as_json()
            print json.dumps(response)
            return HttpResponse(json.dumps(response), content_type='application/json', status=200)
        except:
            response["message"] = "Invalid referral code"
            print "aisa kono user nahi"
            response["user"] = {}
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

@csrf_exempt
def get_user(request,id):
    if request.method == 'GET':
        response = {}
        try:
            curr_user = Users.objects.get(pk=int(id))
            response["user"] = curr_user.as_json()
            if curr_user.referred_by is not None:
                referral_user = Users.objects.get(pk=int(curr_user.referred_by))
                response["user"]["referred_by"] = str(referral_user.name)
            return HttpResponse(json.dumps(response), content_type='application/json', status=200)
        except:
            response["message"] = "Invalid user id"
            response["user"] = {}
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

@csrf_exempt
def all_users(request):
    if request.method == 'GET':
        response = {}
        all_users_array = []
        all_users_data = Users.objects.all().order_by("-referral_score")
        for each_user in all_users_data:
            all_users_array.append(each_user.as_json())

        response["users"] = all_users_array
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)



