from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from dkfriend_back.settings import (
    SIMPLE_JWT,
    SECRET_KEY,
    KAKAO_ADMIN_KEY,
    KAKAO_REST_API_KEY,
    SEND_URI,
)
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views import View
from json.decoder import JSONDecodeError
from booking.models import *
from booking.serializers import *
from .serializers import *
from .utils import make_signature
from .models import Authentication
from django.core.mail import EmailMessage
import jwt
import requests
import json
import time
import random

BASE_URL = "https://beerbuddy2023.com/"
# --- token refresh ---


class RefreshTokenAuthentication(JWTAuthentication):
    # 쿠키의 refresh 토큰을 인식하여 인증여부 판단
    def authenticate(self, request):
        refresh_token = request.COOKIES.get(SIMPLE_JWT["AUTH_COOKIE"], None)

        if refresh_token is None:
            raise AuthenticationFailed("refresh token이 없습니다")

        token_obj = RefreshToken(refresh_token)
        try:
            # 토큰이 블랙리스트에 있는지 확인 -> 있다면 에러 발생
            token_obj.check_blacklist()
        except TokenError:
            raise AuthenticationFailed("유효하지 않은 refresh token입니다")

        # 토큰 decode
        decoded_jwt = jwt.decode(
            jwt=refresh_token,
            key=SECRET_KEY,
            algorithms=["HS256"],
        )

        # 해당 정보로 현재 user 식별
        try:
            user = self.user_model.objects.get(
                **{SIMPLE_JWT["USER_ID_FIELD"]: decoded_jwt.get("user_id")}
            )
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed("존재하지 않는 사용자입니다", code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed("활성화 계정이 아닙니다", code="user_inactive")

        # blacklist에 넣기
        token_obj.blacklist()
        # USER 객체와, VALIDATE된 TOKEN 반환
        return user, refresh_token


class TokenRefreshView(APIView):
    authentication_classes = [RefreshTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = RefreshToken.for_user(request.user)
        new_access = str(refresh.access_token)
        new_refresh = str(refresh)
        response = Response(
            dict(access_token=new_access),
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            SIMPLE_JWT["AUTH_COOKIE"],
            new_refresh,
            httponly=True,
            secure=False,
        )
        return response


class email(APIView):
    def send_email(self, email, auth_number):
        timestamp = str(int(time.time() * 1000))
        
        title = f'[대관친구] 회원 인증 번호'
        content = f"""
            안녕하세요 대관친구입니다. 인증메일이 도착했습니다.
            5분 안에 입력해주시기 바랍니다. 
            인증 번호: {auth_number}
            """

        # 이메일 보내기
        email = EmailMessage(
            title,  # 이메일 제목
            content,  # 내용
            to=[email],
        )
        email.send()

        return timestamp


    def post(self, request, *args, **kwargs):
        data_ = json.dumps(request.data)
        data = json.loads(data_)
        try:
            print("try")
            input_email = data['email']
            auth_num = random.randint(10000, 100000)  # 랜덤숫자 생성, 5자리로 계획하였다.
            auth_mobile = Authentication.objects.get(
                email=input_email)
            auth_mobile.auth_number = auth_num
            auth_mobile.save()
            timestamp = self.send_email(email=input_email, auth_number=auth_num)
            print("done1: ", timestamp)
            return JsonResponse({'message': '인증번호 발송완료', '전송시간': timestamp, 'auth_num': auth_num}, status=200)
        except Authentication.DoesNotExist:  # 인증요청번호 미 존재 시 DB 입력 로직 작성
            Authentication.objects.create(
                email=input_email,
                auth_number=auth_num,
            ).save()
            timestamp = self.send_email(email=input_email, auth_number=auth_num)
            print("done2: ", timestamp)
            return JsonResponse({'message': '인증번호 발송 및 DB 입력완료', '전송시간': timestamp, 'auth_num': auth_num}, status=200)


# ---회원가입---
class SignupPost(APIView):
    def post(self, request, *args, **kwargs):

        phone_number = request.data.get("phone_number", None)
        email = request.data.get("email", None)

        if phone_number is None or email is None:
            return Response({"message": "다시 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        user1 = User.objects.filter(phone_number=phone_number).first()
        user2 = User.objects.filter(email=email).first()

        if user1 is not None:
            return Response({"message": "이미 가입된 전화번호입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user2 is not None:
            return Response({"message": "이미 가입된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            new_refresh = RefreshToken.for_user(user)
            new_access = str(new_refresh.access_token)

            response = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입에 성공하였습니다.",
                    "jwt_token": {
                        "access_token": new_access,
                    },
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                SIMPLE_JWT["AUTH_COOKIE"],
                new_refresh,
                httponly=True,
                secure=False,
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtraSignup(APIView):
    # 카카오 회원가입시 추가 정보 입력
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(
            {"message": "카카오 로그인이 되어있지 않아 추가정보 입력 실패"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ---로그인---
class SigninPost(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data["phone_number"]
        password = request.data["password"]
        user = User.objects.filter(phone_number=phone_number).first()

        # 존재하지 않는 유저일 경우
        if user is None:
            return Response(
                {"message": "존재하지않는 사용자입니다. 회원가입을 해주세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 비밀번호만 틀린 경우
        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 존재하는 사용자일 경우
        if user is not None:
            serializer = SigninSerializer(request.data)
            # 새로운 액세스 토큰인 refresh token 발급
            new_refresh = RefreshToken.for_user(user)
            new_access = str(new_refresh.access_token)
            response = Response(
                {
                    "user": serializer.data,
                    "message": "로그인에 성공하였습니다",
                    "jwt_token": {
                        "access_token": new_access,
                    },
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                SIMPLE_JWT["AUTH_COOKIE"],
                new_refresh,
                httponly=True,
                secure=False,
            )
            return response
        return Response(
            {"message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
        )


class KakaoSignin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = f"{BASE_URL}accounts/kakao/callback/"


def kakao_signin(request):
    KAKAO_CALLBACK_URI = f"{BASE_URL}accounts/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    code = request.GET.get("code")
    redirect_uri = f"{BASE_URL}accounts/kakao/callback/"

    # access token 요청
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={redirect_uri}&code={code}"
    )
    token_req_json = token_req.json()

    # 토큰 요청시 에러 발생 확인
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)

    # access token 으로 사용자 정보 얻기
    access_token = token_req_json.get("access_token")
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")

    # 카카오 계정에서 가져올 정보
    email = kakao_account.get("email", None)
    if email is None:
        return Response(
            {"message": "카카오톡에 연동된 이메일이 존재하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST
        )
    kakao_id = profile_json.get("id")
    profile = kakao_account.get("profile")
    user_nickname = profile.get("nickname")
    user_image = profile.get("thumbnail_image_url")

    try:
        # 소셜로그인으로 연동된 해당 이메일의 유저가 있는지 확인
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)

        # 있는데 카카오계정이 아니어도 에러
        if social_user.provider != "kakao":
            return JsonResponse(
                {"message": "카카오 계정이 아닙니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 로그인 진행
        data = {"access_token": access_token, "code": code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/signin/finish/", data=data)
        if accept.status_code != 200:
            return JsonResponse(
                {"message": "카카오계정으로 로그인할 수 없습니다"}, status=accept.status_code
            )
        accept_json = accept.json()
        accept_json.pop("user", None)
        refresh_token = accept_json.pop("refresh", None)

        response = JsonResponse(accept_json, status=status.HTTP_200_OK)
        response.set_cookie(
            SIMPLE_JWT["AUTH_COOKIE"],
            refresh_token,
            httponly=True,
            secure=True,
        )
        return response

    except User.DoesNotExist:
        # 카카오 로그인으로 가입된 유저가 없으면  => 새로 회원가입 & 해당 유저의 jwt 발급
        data = {"access_token": access_token, "code": code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/signin/finish/", data=data)
        if accept.status_code != 200:
            return JsonResponse(
                {"message": "카카오계정으로 로그인할 수 없습니다"}, status=accept.status_code
            )

        # 유저에 가져온 정보 저장
        user = User.objects.filter(email=email)
        user.update(
            user_nickname=user_nickname,
            user_image=user_image,
            is_active=True,
            kakao_id=kakao_id,
        )

        accept_json = accept.json()
        accept_json.pop("user", None)
        refresh_token = accept_json.pop("refresh", None)

        response = JsonResponse(accept_json, status=status.HTTP_200_OK)
        response.set_cookie(
            SIMPLE_JWT["AUTH_COOKIE"],
            refresh_token,
            httponly=True,
            secure=True,
        )
        return response

    except SocialAccount.DoesNotExist:
        # User는 있는데 SocialAccount가 없을 때
        return JsonResponse(
            {"message": "카카오 연동계정이 아닙니다"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# 로그아웃
class SignoutPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.kakao_id is not None:
            auth = request.headers.get("Authorization", None)
            header = {"Authorization": auth,
                      "Content-Type": "application/x-www-form-urlencoded"}
            logout_res = requests.post(
                "https://kapi.kakao.com/v1/user/logout", headers=header)
            kakao_id = logout_res.json().pop("id", None)

            if kakao_id != request.user.kakao_id:
                return Response({"message": "로그아웃 과정에서 문제가 발생했습니다."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = Response({"message": "로그아웃 되었습니다."},
                                status=status.HTTP_202_ACCEPTED)

        # 로그아웃 = 쿠키에 저장된 토큰 만료시키기
        response.set_cookie("refresh_token", expires=0)
        return response


# ---탈퇴하기---
class LeavePost(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            user = request.user
            kakao_id = user.kakao_id

            # 소셜계정일 경우
            if kakao_id is not None:
                url = "https://kapi.kakao.com/v1/user/unlink"
                headers = {"Authorization": f"KakaoAK {KAKAO_ADMIN_KEY}"}
                data = {"target_id_type": "user_id", "target_id": kakao_id}
                res = requests.post(url, headers=headers, data=data)

                # 소셜계정 연결 끊기 실패
                if kakao_id != res.json().get("id"):
                    return Response(
                        {"message": "연결 끊기 및 탈퇴에 실패하였습니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # db에서 일반/소셜 계정 삭제 및 로그아웃
            user.delete()
            response = Response(
                {"message": "연결 끊기 및 탈퇴되었습니다."}, status=status.HTTP_202_ACCEPTED
            )
            response.set_cookie("refresh_token", expires=0)
            return response

        except:
            Response(
                {"message": "연결 끊기 및 탈퇴에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


# --- 전체 예약 리스트 페이지 ---
class BookList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        bookings = Booking.objects.filter(user=user_serializer.data["id"])
        serializer = BookingSerializer(bookings, many=True)

        return Response(
            {"bookingList": serializer.data, "message": "예약 리스트 로드 성공"},
            status=status.HTTP_200_OK,
        )


# --- 유저정보 페이지 ---
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserInfoSerializer(request.user)
        return Response(
            {"user": user_serializer.data, "message": "마이 페이지 로드 성공"},
            status=status.HTTP_200_OK,
        )


# --- 비밀번호 찾기 ---
class PwPost(APIView):
    def post(self, request):
        # 인증된 핸드폰 번호로 id 찾기
        phone_number = request.data["phone_number"]
        email = request.data["email"]

        user1 = User.objects.get(email=email)
        if user1 is None:
            return Response(
                {"message": "등록되지 않은 아이디입니다. 회원가입 먼저 해주세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user2 = User.objects.get(phone_number=phone_number)
        if user2 is None:
            return Response(
                {"message": "등록되지 않은 전화번호입니다. 회원가입 먼저 해주세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user1 != user2:
            return Response(
                {"message": "잘못된 아이디/전화번호를 입력하셨습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 비밀번호 reset 프론트 주소로 변경하기
        return Response(
            {"message": "존재하는 회원입니다. 비밀번호 초기화 화면으로 이동해주세요"},
            status=status.HTTP_200_OK,
        )


# -- 비밀번호 초기화 ---
class ResetPw(APIView):
    def post(self, request, pk):
        # 비밀번호 아예 잃어버린 경우
        if not request.user.is_authenticated:
            if not User.objects.filter(id=pk).exists():
                return Response(
                    {"message": "존재하는 회원이 아닙니다"}, status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.filter(id=pk).get()
        else:
            user = request.user
            # 로그인되어 있는 경우
            if user.id != pk:
                return Response(
                    {"message": "현재 로그인된 회원 정보만 수정할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED,
                )

        # 비밀번호 초기화
        new_password = request.data.get("new_password", None)
        if new_password is None:
            return Response(
                {"message": "새로 입력된 비밀번호가 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "비밀번호 초기화에 성공하셨습니다."},
            status=status.HTTP_200_OK,
        )
