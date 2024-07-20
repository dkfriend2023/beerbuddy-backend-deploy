from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('<int:pk>/', RestaurantDetail.as_view()),
    path('', RestaurantList.as_view()),
] 

urlpatterns = format_suffix_patterns(urlpatterns)