from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
  path('<int:pk>/', BookingPost.as_view()),
  path('<int:pk>/done/', BookingDetail.as_view()),
] 

urlpatterns = format_suffix_patterns(urlpatterns)