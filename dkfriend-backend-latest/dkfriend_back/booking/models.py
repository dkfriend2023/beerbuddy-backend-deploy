from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


# 예약한 식당 정보
class Booking(models.Model):
    user = models.ForeignKey(
        "accounts.User", verbose_name="예약자 이름", on_delete=models.CASCADE, null=True
    )
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", verbose_name="식당 이름", on_delete=models.CASCADE
    )
    date = models.DateField("예약 날짜", auto_now=False, auto_now_add=False)
    time = models.TimeField("예약 시간", auto_now=False, auto_now_add=False)
    book_number = models.UUIDField("예약 번호", default=uuid.uuid4)
    people_num = models.PositiveSmallIntegerField(
        "예약 인원", validators=[MinValueValidator(8), MaxValueValidator(200)]
    )
    meeting_name = models.CharField("모임명", max_length=15)
    description = models.TextField("요청 사항", blank=True, max_length=100)

    def __str__(self):
        return self.meeting_name
