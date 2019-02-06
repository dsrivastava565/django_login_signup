from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# from .models import *
from django.contrib.auth import authenticate, login, logout

import json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        user = User.objects.create(username=username,password=password)
        return JsonResponse({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
    token,_ = Token.objects.get_or_create(user=user)


    return JsonResponse({'token': token.key},
                    status=HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    msg = {'msg':'success'}
    return JsonResponse(data=msg,status=200,safe=False)


def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = User.objects.filter(username = username,password = password)
        print(user)
        if user:
            return JsonResponse({'msg':'user_found'},safe = False)
        else:
            return JsonResponse({'msg':'no_user'},safe = False)
    else:
        JsonResponse({'msg':'wrong method'})

# def success(request):
#     pass

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'msg':'successfully logout'})

def register(request):
    if request.method == 'POST':
        data  = json.loads(request.body)
        username = data['username']
        password = data['password']
        if username:
            create = User.objects.create(username = username,password = password)
            return JsonResponse({'msg':'succesfully created'},safe =False,status=201)