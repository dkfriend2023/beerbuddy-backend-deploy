from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=email,
            user_nickname=str(email).split("@")[0],
            phone_number=kwargs["phone_number"],
            uni=kwargs["uni"],
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
            uni="연세대학교",
            phone_number="01000000000",
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser


# 사용자 정보
class User(AbstractBaseUser, PermissionsMixin):
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    email = models.EmailField(
        max_length=40, unique=True, null=False, blank=False)
    user_image = models.FileField(
        "프로필 이미지",
        upload_to="users",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "png", "pdf", "svg"])],
    )
    user_nickname = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )
    uni = models.CharField("소속 대학교", max_length=20,
                           help_text="대학교 풀네임(ex, OO대학교)")
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r"^010?[1-9]\d{3}?\d{4}$")],
    )
    like_restaurant = models.ManyToManyField(
        "restaurant.Restaurant",
        verbose_name="찜한 식당 목록",
        related_name="like_users",
        blank=True,
        default=[],
    )
    kakao_id = models.PositiveIntegerField(
        "카카오 연동 계정 pk", blank=False, null=True)

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.user_nickname


class Authentication(models.Model):
    phone_number = models.CharField('휴대폰 번호', max_length=30)
    auth_number = models.CharField('인증번호', max_length=30)

    class Meta:
        db_table = 'authentications'  # DB 테이블명
        verbose_name_plural = "휴대폰인증 관리 페이지"  # Admin 페이지에서 나타나는 설명
