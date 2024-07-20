from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('', MainList.as_view()),
    path('groups/<int:pk>/', GroupDetail.as_view()),
] 

urlpatterns = format_suffix_patterns(urlpatterns)