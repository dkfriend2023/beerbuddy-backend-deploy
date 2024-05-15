from django.shortcuts import get_object_or_404, redirect
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from restaurant.serializers import *
from restaurant.models import *
from main.serializers import *
from main.models import *
from accounts.serializers import *


# 예약 페이지
class BookingPost(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, model):
        return get_object_or_404(model, pk=pk)

    # 식당 유의사항 detail 보기
    def get(self, request, pk, format=None):
        users_serializer = UserSerializer(request.user)

        # 해당 식당 정보
        restaurant = self.get_object(pk, Restaurant)
        restaurant_serializer = RestaurantsSerializer(restaurant)

        # 해당 식당 예약 주의 사항
        notice = self.get_object(pk, Notice)
        notice_serializer = NoticeSerializer(notice)

        return Response(
            {
                "user": users_serializer.data,
                "restaurant": restaurant_serializer.data,
                "notice": notice_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # 예약 정보 입력
    def post(self, request, pk):
        request.data["user"] = request.user.id
        restaurant = Restaurant.objects.get(id=pk)
        request.data["restaurant"] = restaurant.id
        serializer = BookingSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            booking_instance = serializer.save()

            title = f'[대관친구] {request.user.user_nickname} {request.data.get("date", None)}{request.data.get("time", None)} 예약 완료'
            content = f"""
            예약자: {request.user.user_nickname}
            예약명: {request.data.get("meeting_name", None)}
            식당명: {restaurant.name}
            예약 날짜: {request.data.get("date", None)}
            예약 시간: {request.data.get("time", None)}
            예약 인원: {request.data.get("people_num", None)}
            예약 번호: {booking_instance.book_number}
            요청 사항: {request.data.get("description", None)}
            """

            # 이메일 보내기
            email = EmailMessage(
                title,  # 이메일 제목
                content,  # 내용
                to=["beerbuddy@naver.com"],
            )
            email.send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 예약 완료 페이지
class BookingDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Booking, pk=pk)

    def get(self, request, pk, format=None):
        users_serializer = UserSerializer(request.user)

        # 해당 예약 정보 가져오기
        booking = self.get_object(pk)
        booking_serializer = BookingSerializer(booking)

        # 전체 광고 정보 가져오기
        ads = Ad.objects.all()
        ads_serializer = AdsSerializer(ads, many=True)

        return Response(
            {
                "user": users_serializer.data,
                "booking": booking_serializer.data,
                "ads": ads_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
