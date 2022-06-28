from dataclasses import field, fields
from email.mime import image
from pyexpat import model
from typing_extensions import Self
from requests import request
from rest_framework import serializers
from exam.models import ToDOList, ToDouser
from drf_extra_fields.fields import Base64ImageField
import base64
from django.core.files.base import ContentFile

class UserRegistrationSerializer(serializers.ModelSerializer):


    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = ToDouser
        fields = ['email','fullname','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):

        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password Doesnot match with confirm password")

        return attrs

    def create(self, validate_data):
        return ToDouser.objects.create_user(**validate_data)



class UserLoginSerializer(serializers.ModelSerializer):

    
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = ToDouser
        fields = ['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDouser
        fields = ['id','fullname','email']

class TodoListSerializer(serializers.ModelSerializer):
    
    def from_native(self, image):

        if isinstance(image, basestring) and image.startswith('data:image'):
            format, imgstr = image.split(';base64,')  
            ext = format.split('/')[-1]  

            img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
       
        image = img
        print("here")
    class Meta:
        model = ToDOList
        fields = ['name','image','deadline','description','uploaded_by']

        
            

