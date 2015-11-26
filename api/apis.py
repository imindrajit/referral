from django.shortcuts import render_to_response, RequestContext, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import urllib2
from referral.settings import DOMAIN
from referral_coupon.models import Users, Coupons, UsedCoupons

def verify_name(name):
    if len(name) > 50:
        return False
    if re.match("^[A-Za-z]*$", name):
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


@csrf_exempt
def user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print json.dumps(body)
        if not body["name"] or not body["email"]:
            return HttpResponse(content="", status=400)
        response = {}
        if verify_name(body["name"]) == False:
            response["message"] = "Please enter a valid name"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        if verify_email(body["email"]) == False:
            response["message"] = "Please enter a valid email"
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        print "naam pata done"
        referred_by_user = None
        referred_by_user_referral_code = body["referred_by_code"]
        if referred_by_user_referral_code.strip() == "":
            try:
                referred_by_user = verify_referral_code(referred_by_user_referral_code)
            except:
                response["message"] = "Please enter a valid referral code"
                return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        else:
            pass

        newUser = Users()
        newUser.name = body["name"]
        newUser.email = body["email"]
        if referred_by_user:
            newUser.referred_by = referred_by_user
            newUser.referred_by_code = referred_by_user["referred_by_code"]
        newUser.save()
        response['message'] = "User successfully added"
        response['user'] = newUser
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
