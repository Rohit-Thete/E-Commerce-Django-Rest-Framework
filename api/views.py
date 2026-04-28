from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import RegisterSerializer, LoginSerializer,UserReadSerializer,UserUpdateSerializer
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from .permissions import *


# Create your views here.

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "msg": "User Created",
                "user": {"username": user.username, "email": user.email},
            },
            status=201,
        )

    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data["user"]
        return Response(
            {
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
                "user": {"username": user.username, "email": user.email},
            },
            status=200,
        )

    return Response(serializer.errors, status=400)

class UserView(APIView):
    permission_classes = [IsOwner,IsAuthenticated]
    def get(self,request):
        user = request.user
        data = User.objects.get(username = user.username)

        serializer =UserReadSerializer(data)
        return Response(serializer.data,status=200)
    
    def put(self,request):
        user = request.user
        self.check_object_permissions(request, user)
        serializer = UserUpdateSerializer(user,data = request.data ,partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        
        return Response(serializer.errors,status=400)
    



