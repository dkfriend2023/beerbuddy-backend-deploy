from django.contrib import admin
from .models import *


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'meeting_name',
    'book_number',
    'restaurant',
    'date',
  ]
  
  list_display_links = ['meeting_name']