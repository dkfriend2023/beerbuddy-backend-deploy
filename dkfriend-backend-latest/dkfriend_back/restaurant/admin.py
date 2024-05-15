from django.contrib import admin
from .models import *
import admin_thumbnails


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "restaurant",
        "created_at",
    ]

    list_display_links = ["restaurant"]


@admin_thumbnails.thumbnail("image")
class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Restaurant)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "groups",
        "name",
    ]
    inlines = [
        ReviewInLine,
    ]
    list_display_links = ["name"]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "restaurant",
        "name",
    ]
    list_display_links = ["name"]


@admin.register(Feature)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "restaurant",
    ]
    list_display_links = ["restaurant"]


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "restaurant",
    ]
    list_display_links = ["restaurant"]
