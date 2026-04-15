from django.contrib import admin
from .models import Category, Complaint, ComplaintAttachment, Resolution, Feedback, Notification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']


class ComplaintAttachmentInline(admin.TabularInline):
    model = ComplaintAttachment
    extra = 0
    readonly_fields = ['original_name', 'uploaded_at']


class ResolutionInline(admin.TabularInline):
    model = Resolution
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_id', 'title', 'category', 'status', 'priority', 'submitted_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['complaint_id', 'title', 'description', 'submitted_by__username']
    readonly_fields = ['complaint_id', 'created_at', 'updated_at', 'resolved_at']
    inlines = [ComplaintAttachmentInline, ResolutionInline]
    ordering = ['-created_at']

    fieldsets = (
        ('Complaint Info', {'fields': ('complaint_id', 'title', 'description', 'category', 'location')}),
        ('Status & Priority', {'fields': ('status', 'priority', 'is_anonymous', 'expected_resolution_date')}),
        ('Assignment', {'fields': ('submitted_by', 'assigned_to')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'resolved_at')}),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'submitted_by', 'rating', 'created_at']
    list_filter = ['rating']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read']
    readonly_fields = ['created_at']
