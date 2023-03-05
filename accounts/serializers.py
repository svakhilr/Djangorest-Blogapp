from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerialiser(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email    = serializers.EmailField(max_length=25)
    password =  serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        
        password = attrs.get('password')
        repeat_password = attrs.get('repeat_password')
        if password == repeat_password:
            return attrs
        raise serializers.ValidationError("password dosen't match")
    
    def create(self, validate_data):
        
        username= validate_data['username']
        
        
        email= validate_data['email']
        
        password= validate_data['password']
        user= User.objects.create_user(username=username,email=email,password=password)
        
        return user
