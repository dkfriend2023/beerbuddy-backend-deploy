from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data.get("password"),
            user_nickname=validated_data.get("user_nickname"),
            email=validated_data.get("email"),
            user_image=validated_data.get("user_image"),
            like_restaurant=validated_data.get("like_restaurant"),
            phone_number=validated_data.get("phone_number"),
            uni=validated_data.get("uni"),
            kakao_id=validated_data.get("kakao_id"),
        )
        return user


class SigninSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "user_image", "user_nickname",
                  "uni", "phone_number", "kakao_id", "like_restaurant"]
