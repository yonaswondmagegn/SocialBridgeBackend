from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
import datetime
from django.utils import timezone
from djoser.views import TokenCreateView

User = get_user_model()

class RegisterUser(APIView):
    def post(self,request):
        phonenumber = request.data.get("phonenumber")
        username = request.data.get('username')
       
        try:
            if not phonenumber:
                raise ValueError('Phone Number Is Requred')
            
            user,created = User.objects.get_or_create(phonenumber = phonenumber)
            if created and username:
                user.username = username
                user.save()

            refresh = RefreshToken.for_user(user)
            return Response(data={
                 'refresh': str(refresh),
                 'access': str(refresh.access_token),
            },status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(data={'error':'something wrong happend'},status=status.HTTP_400_BAD_REQUEST)
