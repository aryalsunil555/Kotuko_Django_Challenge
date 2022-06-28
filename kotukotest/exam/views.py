import email
import json
from django.http import HttpResponse
from django.shortcuts import render
from requests import request
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from exam.models import ToDOList

from exam.serializers import  TodoListSerializer, UserLoginSerializer, UserRegistrationSerializer, UserProfileSerializer
from exam.renderers import UserRenderer
from django.db.models import Exists, OuterRef
# Create your views here.

#Task 1 Login and Register
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Register API
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):


        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)

            else:
                return Response({'errors':{'non_field_errors':['Email or Password is Incorrect']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        
        serializer = UserProfileSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

#Task 2 Add todo List by user
class AddTodoListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        
        serializer = TodoListSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Task 3 see own todo list added by user
class BrowseMyTodoList(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = TodoListSerializer

    def get_queryset(self):
        
        user = self.request.user
        myprods = ToDOList.objects.filter(uploaded_by=user)
        return myprods.order_by('-creation_date')




class TodoDetail(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return ToDOList.objects.get(pk=pk)
        except ToDOList.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mytodo = self.get_object(pk)
        if mytodo.uploaded_by == request.user:

            serializer = TodoListSerializer(mytodo)
            return Response(serializer.data)
        else:
            return Response({'msg':"You are not authorized to view this product"},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        mytodo = self.get_object(pk)
        if mytodo.uploaded_by == request.user:
            serializer = TodoListSerializer(mytodo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':"You are not authorized to update this product"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mytodo = self.get_object(pk)
        if mytodo.uploaded_by == request.user:
            mytodo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg':"You are not authorized to delete this product"},status=status.HTTP_400_BAD_REQUEST)
