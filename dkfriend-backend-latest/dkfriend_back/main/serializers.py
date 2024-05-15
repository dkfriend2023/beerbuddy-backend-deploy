from rest_framework import serializers
from .models import *


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
