from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import  authenticate
from .serializers import UserSerialiser

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UsersAPIView(APIView):
    def get(self, request):
        
        users = User.objects.filter(is_superuser=False)
        serializer = UserSerialiser(users, many = True)
        return Response(serializer.data)
        
    
    def post(self, request):
        serializer = UserSerialiser(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)
    
class UserloginView(APIView):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(username=username,password=password)
        if user:
            tokens=get_tokens_for_user(user)
            return Response({"success":"succesfully login","TOKEN":tokens},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":"invalid credentials"},status=status.HTTP_400_BAD_REQUEST)