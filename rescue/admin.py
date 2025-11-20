from django.contrib import admin
from .models import Shelter, Animal, Report, AdoptionRequest, Update, Notification


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'phone', 'email']
    search_fields = ['name', 'city', 'state']


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'animal_type', 'breed', 'status', 'shelter', 'created_at']
    list_filter = ['animal_type', 'status', 'shelter']
    search_fields = ['name', 'breed', 'description']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'animal_type', 'location', 'status', 'reported_by', 'created_at']
    list_filter = ['report_type', 'animal_type', 'status']
    search_fields = ['location', 'description']


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['animal', 'user', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['animal__name', 'user__username']


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'animal', 'report', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'content']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['shelter', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'shelter__name']
    readonly_fields = ['created_at']


