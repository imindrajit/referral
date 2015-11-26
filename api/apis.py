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

def increment_referral_scores(code):
    users = Users.objects.filter(Q(referral_code=str(code)) | Q(referred_by_code=str(code)))
    for each_user in users:
        each_user.referral_score = each_user.referral_score + 1
        each_user.save()


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

        newUser = Users()
        newUser.name = body["name"]
        newUser.email = body["email"]
        if referred_by_user:
            newUser.referred_by = int(referred_by_user["id"])
            newUser.referred_by_code = referred_by_user["referral_code"]
        newUser.save()
        if referred_by_user:
            increment_referral_scores(referred_by_user["referral_code"])
        response['message'] = "User successfully added"
        response['user'] = newUser.as_json()
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



