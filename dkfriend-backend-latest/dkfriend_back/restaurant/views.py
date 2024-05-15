from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import *
from .models import *


# 식당별 세부페이지
class RestaurantDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk, model):
        return get_object_or_404(model, pk=pk)

    def get(self, request, pk, format=None):
        # 해당 식당 정보
        restaurant = self.get_object(pk, Restaurant)
        restaurant_serializer = RestaurantsSerializer(restaurant)
        # 해당 식당 편의시설
        feature = self.get_object(pk, Feature)
        feature_serializer = FeaturesSerializer(feature)
        # 해당 식당 메뉴
        menu = self.get_object(pk, Menu)
        menu_serializer = MenuSerializer(menu)
        # 해당 식당 예약 주의사항
        notice = self.get_object(pk, Notice)
        notice_serializer = NoticeSerializer(notice)
        # 해당 식당 전체 리뷰
        # review = self.get_object(pk, Review)
        # review_serializer = ReviewsSerializer(review)

        return Response(
            {
                "restaurant": restaurant_serializer.data,
                "feature": feature_serializer.data,
                "menu": menu_serializer.data,
                "notice": notice_serializer.data,
                # "review": review_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # 찜하기 기능 - 하트 눌렀을 경우
    def post(self, request, pk, format=None):
        # 찜할 식당 정보
        restaurant = self.get_object(pk, Restaurant)
        user = request.user

        # 이미 찜한 경우 - 찜 취소
        if user.like_restaurant.filter(id=pk).exists():
            user.like_restaurant.remove(restaurant)
            return Response({"message": "찜 취소"}, status=status.HTTP_201_CREATED)

        # 찜 안되어 있는 경우 - 찜 추가
        user.like_restaurant.add(restaurant)
        return Response({"message": "찜"}, status=status.HTTP_201_CREATED)


# 식당 전체 리스트
class RestaurantList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None, **kwargs):
        restaurants = Restaurant.objects.all()
        restaurants_serializer = RestaurantsSerializer(restaurants, many=True)

        return Response({
                "restaurants": restaurants_serializer.data,
            }, status=status.HTTP_200_OK)