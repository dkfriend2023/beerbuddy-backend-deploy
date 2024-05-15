from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator


# ---상권별 식당---
class Restaurant(models.Model):
    groups = models.ForeignKey(
        "main.Group", verbose_name="상권 이름", on_delete=models.CASCADE
    )
    name = models.CharField("식당 이름", max_length=50)
    image = models.FileField(
        "식당 이미지",
        upload_to="restaurants",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "png", "pdf", "svg"])],
    )
    deposit = models.PositiveIntegerField("보증금", default=0)
    open_hour = models.TimeField("오픈 시간")
    close_hour = models.TimeField("마감 시간")
    available = models.BooleanField("예약 가능 여부", default=False)
    empty_seat = models.PositiveIntegerField("현재 빈 좌석수", default=0)
    total_seat = models.PositiveIntegerField("총 좌석수", default=0)
    is_ad = models.BooleanField("광고 신청 여부", default=False)
    tel = models.CharField("대표 번호", max_length=13, unique=True)
    description = models.TextField("식당 설명", blank=True, max_length=500)
    location = models.TextField("식당 주소")

    def __str__(self):
        return self.name


# ---식당별 메뉴---
class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, verbose_name="식당 이름", on_delete=models.CASCADE
    )
    name = models.CharField("음식 이름", max_length=50)
    is_recommended = models.BooleanField("대표 음식 여부", default=False)
    price = models.PositiveIntegerField("음식 가격", default=0)
    image = models.FileField(
        "음식 사진",
        upload_to="Restaurant/menu",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "png", "pdf", "svg"])],
    )
    description = models.TextField("음식 소개", blank=True, max_length=100)

    def __str__(self):
        return self.name


# ---식당별 리뷰---
class Review(models.Model):
    user = models.ForeignKey(
        "accounts.User", verbose_name="작성자", on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant, verbose_name="식당 이름", on_delete=models.CASCADE
    )
    created_at = models.DateField("리뷰 작성 일시", auto_now_add=True)
    content = models.TextField("리뷰 내용", max_length=200)
    rating = models.PositiveSmallIntegerField(
        "별점", validators=[MinValueValidator(0), MaxValueValidator(5)], default=5
    )
    image = models.FileField(
        "리뷰사진",
        upload_to="reviews",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "png", "pdf", "svg"])],
    )

    def __str__(self):
        return f"{self.restaurant.name}의 리뷰"


# ---식당별 특이사항---
class Feature(models.Model):
    CROWDED_CHOICES = [
        ("CROWDED", "Crowded"),
        ("NEUTRAL", "Neutral"),
        ("QUIET", "Quiet"),
    ]
    restaurant = models.ForeignKey(
        Restaurant, verbose_name="식당 이름", on_delete=models.CASCADE
    )
    totalseats = models.PositiveIntegerField("총 자리 수", default=1)
    floor = models.PositiveSmallIntegerField("층 수", default=1)
    whetherdeposit = models.BooleanField("보증금 여부", default=False)
    parking = models.BooleanField("주차 가능 여부", default=False)
    crowded = models.CharField(
        "분위기", max_length=10, choices=CROWDED_CHOICES, default="QUIET"
    )
    tvscreen = models.BooleanField("스크린 여부", default=False)
    minimum_order = models.TextField("최소 주문 기준", max_length=150, blank=True)
    limited_time = models.PositiveIntegerField("대관 제한시간", default=1)

    def __str__(self):
        return f"{self.restaurant.name}의 특이사항"


# ---식당별 예약시 주의 사항---
class Notice(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, verbose_name="식당 이름", on_delete=models.CASCADE
    )
    max_time = models.PositiveSmallIntegerField(
        "최대 이용 시간", default=0, blank=True)
    description = models.TextField("추가 유의 사항", blank=True)

    def __str__(self):
        return f"{self.restaurant.name}의 예약시 주의사항"
