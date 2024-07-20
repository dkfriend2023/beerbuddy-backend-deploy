from django.contrib import admin
from .models import *


@admin.register(Ad)
class AdsAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'company_name',
    'link',
  ]
  
  list_display_links = ['company_name']
  
@admin.register(Group)
class GroupsAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'name',
  ]
  
  list_display_links = ['name']