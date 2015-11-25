from django.shortcuts import render_to_response, RequestContext, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import urllib2
from referral.settings import DOMAIN


def verify_email(mail):
    if re.match("[\w\.\-]*@[\w\.\-]*\.\w+", str(mail)):
        url = DOMAIN+'/api/v1/index'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)

@csrf_exempt
def user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if not body["name"] or not body["email"]:
            return HttpResponse(content="", status=400)
        response = {}
        verify_name(body["name"])
        verify_email(body["email"])
        response['code'] = 700
        response['message'] = "Adding Done"
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    elif request.method == 'GET':
        response = {}
        response['code'] = 200
        response['message'] = "Done"
        return HttpResponse(json.dumps(response), content_type='application/json')