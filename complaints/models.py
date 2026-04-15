from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='file-text', help_text='Lucide icon name')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    complaint_id = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='complaints')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    location = models.CharField(max_length=200, blank=True, help_text='Where did this issue occur?')
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    expected_resolution_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.complaint_id}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.complaint_id:
            year = timezone.now().year
            count = Complaint.objects.filter(created_at__year=year).count() + 1
            self.complaint_id = f"PSU-{year}-{count:04d}"
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def status_percentage(self):
        percentages = {
            'pending': 10,
            'under_review': 30,
            'in_progress': 60,
            'resolved': 100,
            'closed': 100,
            'rejected': 0,
        }
        return percentages.get(self.status, 0)

    @property
    def status_color(self):
        colors = {
            'pending': 'status-pending',
            'under_review': 'status-review',
            'in_progress': 'status-progress',
            'resolved': 'status-resolved',
            'closed': 'status-closed',
            'rejected': 'status-rejected',
        }
        return colors.get(self.status, 'status-pending')

    @property
    def priority_color(self):
        colors = {
            'low': 'priority-low',
            'medium': 'priority-medium',
            'high': 'priority-high',
            'urgent': 'priority-urgent',
        }
        return colors.get(self.priority, 'priority-medium')

    def has_feedback(self):
        return hasattr(self, 'feedback')


class ComplaintAttachment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/')
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_name} - {self.complaint.complaint_id}"

    @property
    def is_image(self):
        return self.original_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))


class Resolution(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='resolutions')
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='resolutions_made')
    notes = models.TextField()
    action_taken = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True, help_text='Show this update to the complainant')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Resolution for {self.complaint.complaint_id} by {self.resolved_by}"


class Feedback(models.Model):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='feedback')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.complaint.complaint_id} - {self.rating}/5"

    @property
    def stars_range(self):
        return range(1, 6)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
