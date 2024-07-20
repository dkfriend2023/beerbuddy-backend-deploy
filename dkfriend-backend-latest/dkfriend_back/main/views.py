from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from accounts.models import *
from accounts.serializers import *
from restaurant.models import *
from restaurant.serializers import *


# 메인페이지
class MainList(APIView):
    def get_object(self, pk, model):
        return get_object_or_404(model, pk=pk)

    def get(self, request, format=None, **kwargs):
        # 유저 정보
        users_serializer = None
        if not request.user.is_anonymous:
            users_serializer = UserSerializer(request.user).data

        # 전체 광고 정보
        ads = Ad.objects.all()
        ads_serializer = AdsSerializer(ads, many=True)
        
        # 전체 상권 정보
        groups = Group.objects.all()
        groups_serializer = GroupsSerializer(groups, many=True)

        return Response(
            {
                "user": users_serializer,
                "ads": ads_serializer.data,
                "groups": groups_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# 상권별 세부페이지
class GroupDetail(APIView):
    def get_object(self, pk, model):
        return get_object_or_404(model, pk=pk)

    def get(self, request, pk, format=None):
        # 유저 정보
        users_serializer = None
        if not request.user.is_anonymous:
            users_serializer = UserSerializer(request.user).data
        
        # 상권별 전체 식당 정보
        restaurants = Restaurant.objects.filter(groups=pk)
        restaurants_serializer = RestaurantsSerializer(restaurants, many=True)

        return Response(
            {
                "user": users_serializer,
                "restaurants": restaurants_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
