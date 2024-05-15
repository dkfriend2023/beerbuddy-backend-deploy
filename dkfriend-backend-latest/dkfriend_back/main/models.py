from django.db import models
from django.core.validators import FileExtensionValidator


# 광고 리스트 정보
class Ad(models.Model):
  company_name = models.CharField("회사 이름", max_length=10)
  link = models.URLField("광고 링크", blank=True)
  image = models.FileField(
    "광고 이미지", upload_to="ads", blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'pdf', 'svg'])])
  
  def __str__(self):
    return f"{self.company_name}의 광고 정보"

# 상권 리스트 정보
class Group(models.Model):
  name = models.CharField("상권 이름", max_length=50)
  image = models.FileField(
    "상권 로고", upload_to="groups", blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'pdf', 'svg'])])
  description = models.TextField("상권 소개", blank=True, max_length=100)

  def __str__(self):
    return self.name