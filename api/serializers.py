from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ["username","email","phone","password"]


    def create(self,validated_data):

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    access = serializers.CharField(read_only = True)
    refresh = serializers.CharField(read_only = True)
   

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username = username,password = password)

        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("User is In-Active")

        refresh = RefreshToken.for_user(user)

        return {
            "user":user,
            "access":str(refresh.access_token),
            "refresh":str(refresh) 
        }
    
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude = ["password"]

class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,required = False)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["username","email","phone","password"]

    
    def validate_username(self,value):
        user = self.instance
        if " " in value:
            raise serializers.ValidationError("Username Cannot contain Spaces")
        if User.objects.filter(username = value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self,value):
        user = self.instance
        if User.objects.filter(email = value).exclude(id = user.id).exists():
            raise serializers.ValidationError("Email already exists")
        
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password",None)

        for attr,value in validated_data.items():
            setattr(instance,attr,value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance

        
