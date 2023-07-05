from django.shortcuts import render
from rest_framework.permissions import AllowAny
from .models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializer import RegisterSeralizer,LoginSerializer,MemberSeralizer
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from.permissions import IsLibrarian


class RegisterView(generics.CreateAPIView):
    qs = User.objects.all()
    serializer_class = RegisterSeralizer


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self,request,*args,**kwargs):
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({"error": "user name doesnot exist"},status=status.HTTP_404_NOT_FOUND)
        
        if check_password(request.data['password'],user.password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_401_UNAUTHORIZED)
        
    
        
class MemberView(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='member')
    serializer_class = MemberSeralizer
    authentication_classes =[TokenAuthentication]
    permission_classes = [IsLibrarian]





            


