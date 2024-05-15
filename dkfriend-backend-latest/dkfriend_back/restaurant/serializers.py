from rest_framework import serializers
from .models import *


# 상권별 식당
class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


# 식당별 메뉴
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


# 식당별 리뷰
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  


# 식당별 특이사항
class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
        

# 식당별 예약시 주의 사항
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'  
