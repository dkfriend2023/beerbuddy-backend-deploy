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
        date_full = request.data.get("date")
        year, month, day = date_full.split("-") if date_full else (None, None, None)
        time_full = request.data.get("time")
        hour = time_full.split(":")[0] if time_full else None
        minute = time_full.split(":")[1] if time_full else None

        # 유효성 검사
        if serializer.is_valid():
            booking_instance = serializer.save()

            title = f'[비어버디] {restaurant.name} - {year}년 {month}월 {day}일 예약 요청 접수'

            content = f"""
                예약 번호: {booking_instance.book_number}
                
                예약자: {request.user.user_nickname}
                
                예약명: {request.data.get("meeting_name", None)}
                
                식당명: {restaurant.name}
                
                예약 일시: {year}년 {month}월 {day}일 {hour}시 {minute}분
                
                예약 인원: {request.data.get("people_num", None)}명
                
                요청 사항: {request.data.get("description", None)}

                해당 예약은 아직 확정되지 않았습니다. 예약 확정 후 별도로 연락드리겠습니다.\n\n"""

            email = EmailMessage(
                title,  # 이메일 제목
                content,  # 이메일 내용
                to=[request.user.email, 'beerbuddy@naver.com', 'dkfriend.official@gmail.com'])
            
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
