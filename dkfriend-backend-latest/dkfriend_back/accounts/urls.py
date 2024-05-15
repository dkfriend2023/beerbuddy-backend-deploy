from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


urlpatterns = [
    path("sign-up/", SignupPost.as_view(), name="sign_up"),
    path("extra-signup/", ExtraSignup.as_view()),
    path("sign-in/", SigninPost.as_view(), name="sign_in"),
    path("sign-out/", SignoutPost.as_view(), name="sign_out"),
    path("user-info/", UserDetail.as_view()),
    path("booking-list/", BookList.as_view()),
    path("leave/", LeavePost.as_view()),
    path("kakao/signin/", kakao_signin, name="kakao_signin"),
    path("kakao/signin/finish/", KakaoSignin.as_view(),
         name="kakao_signin_todjango"),
    path("kakao/callback/", kakao_callback, name="kakao_callback"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("find/pw/", PwPost.as_view(), name="find_pw"),
    path("reset-pw/<int:pk>/", ResetPw.as_view(), name="reset_pw"),
    path("sms/", email.as_view(), name="email"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
