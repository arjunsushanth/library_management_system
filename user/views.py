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
from rest_framework.permissions import  IsAuthenticated
from.permissions import IsLibrarian
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    qs= User.objects.all()
    serializer_class = RegisterSeralizer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({"error": "user name doesnot exist"},status=status.HTTP_404_NOT_FOUND)
        
        if check_password(request.data['password'],user.password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes =[TokenAuthentication] 

    def post(self, request):
        # Get the user's token
        token = request.auth

        if token:
            # Delete the token
            token.delete()
            return Response({'detail': 'Logout successful.'})
        
        return Response({'detail': 'No token found.'}, status=400)
        
          
class MemberView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSeralizer
    authentication_classes =[TokenAuthentication]
    permission_classes = (IsLibrarian)

def update(self, request, *args, **kwargs):
        member = self.get_object()
        serializer = RegisterSeralizer(member, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'successfully updated'}, status=status.HTTP_201_CREATED)

def delete(self,request,*args,**kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

    







            


