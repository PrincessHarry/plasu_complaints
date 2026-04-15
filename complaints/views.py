from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.utils import timezone
from django.conf import settings

from .models import Complaint, ComplaintAttachment, Resolution, Feedback, Notification, Category
from .forms import ComplaintForm, ComplaintFilterForm, FeedbackForm, ResolutionForm
from accounts.models import User


def home(request):
    stats = {
        'total': Complaint.objects.count(),
        'resolved': Complaint.objects.filter(status='resolved').count(),
        'pending': Complaint.objects.filter(status='pending').count(),
        'categories': Category.objects.filter(is_active=True).count(),
    }
    recent_categories = Category.objects.filter(is_active=True)[:6]
    return render(request, 'complaints/home.html', {
        'stats': stats,
        'categories': recent_categories,
    })


@login_required
def dashboard(request):
    user = request.user

    if user.is_admin_user:
        complaints = Complaint.objects.select_related('submitted_by', 'category', 'assigned_to')
        stats = {
            'total': complaints.count(),
            'pending': complaints.filter(status='pending').count(),
            'under_review': complaints.filter(status='under_review').count(),
            'in_progress': complaints.filter(status='in_progress').count(),
            'resolved': complaints.filter(status='resolved').count(),
            'urgent': complaints.filter(priority='urgent').count(),
        }
        recent_complaints = complaints.order_by('-created_at')[:8]
        avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg']
        context = {
            'complaints': recent_complaints,
            'stats': stats,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'is_admin_view': True,
        }

    elif user.is_staff_user:
        assigned = Complaint.objects.filter(assigned_to=user).select_related('submitted_by', 'category')
        stats = {
            'assigned': assigned.count(),
            'pending': assigned.filter(status='pending').count(),
            'in_progress': assigned.filter(status='in_progress').count(),
            'resolved': assigned.filter(status='resolved').count(),
        }
        context = {
            'complaints': assigned.order_by('-created_at')[:8],
            'stats': stats,
            'is_staff_view': True,
        }

    else:
        my_complaints = Complaint.objects.filter(submitted_by=user).select_related('category')
        stats = {
            'total': my_complaints.count(),
            'pending': my_complaints.filter(status='pending').count(),
            'in_progress': my_complaints.filter(Q(status='under_review') | Q(status='in_progress')).count(),
            'resolved': my_complaints.filter(status='resolved').count(),
        }
        context = {
            'complaints': my_complaints.order_by('-created_at')[:8],
            'stats': stats,
            'is_student_view': True,
        }

    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    context['unread_notifications'] = unread_notifications
    return render(request, 'complaints/dashboard.html', context)


@login_required
def complaint_list(request):
    user = request.user
    form = ComplaintFilterForm(request.GET)

    if user.is_admin_user:
        complaints = Complaint.objects.select_related('submitted_by', 'category', 'assigned_to')
    elif user.is_staff_user:
        complaints = Complaint.objects.filter(assigned_to=user).select_related('submitted_by', 'category')
    else:
        complaints = Complaint.objects.filter(submitted_by=user).select_related('category')

    if form.is_valid():
        search = form.cleaned_data.get('search')
        status = form.cleaned_data.get('status')
        priority = form.cleaned_data.get('priority')
        category = form.cleaned_data.get('category')

        if search:
            complaints = complaints.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(complaint_id__icontains=search)
            )
        if status:
            complaints = complaints.filter(status=status)
        if priority:
            complaints = complaints.filter(priority=priority)
        if category:
            complaints = complaints.filter(category=category)

    complaints = complaints.order_by('-created_at')
    paginator = Paginator(complaints, getattr(settings, 'COMPLAINTS_PER_PAGE', 10))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'complaints/complaint_list.html', {
        'page_obj': page_obj,
        'form': form,
        'total_count': complaints.count(),
    })


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    user = request.user

    if not user.is_admin_user and not user.is_staff_user and complaint.submitted_by != user:
        return HttpResponseForbidden("You do not have permission to view this complaint.")

    resolutions = complaint.resolutions.filter(is_public=True) if not user.is_admin_user else complaint.resolutions.all()
    feedback = getattr(complaint, 'feedback', None)
    can_give_feedback = (
        complaint.status == 'resolved' and
        complaint.submitted_by == user and
        feedback is None
    )
    can_manage = user.is_admin_user or user.is_staff_user

    staff_list = User.objects.filter(role='staff') if user.is_admin_user else []

    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'resolutions': resolutions,
        'feedback': feedback,
        'can_give_feedback': can_give_feedback,
        'can_manage': can_manage,
        'resolution_form': ResolutionForm(initial={'new_status': complaint.status}) if can_manage else None,
        'feedback_form': FeedbackForm() if can_give_feedback else None,
        'staff_list': staff_list,
    })


@login_required
def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        files = request.FILES.getlist('attachments')

        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.submitted_by = request.user
            complaint.save()

            for f in files:
                if f.size <= settings.MAX_UPLOAD_SIZE:
                    ComplaintAttachment.objects.create(
                        complaint=complaint,
                        file=f,
                        original_name=f.name
                    )

            # Notify admins
            admins = User.objects.filter(role='admin')
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    complaint=complaint,
                    title='New Complaint Filed',
                    message=f'A new complaint "{complaint.title}" has been filed by {request.user.get_full_name() or request.user.username}.'
                )

            messages.success(request, f'Complaint filed successfully! Your complaint ID is {complaint.complaint_id}.')
            return redirect('complaint_detail', pk=complaint.pk)
    else:
        form = ComplaintForm()

    return render(request, 'complaints/file_complaint.html', {'form': form})


@login_required
def add_resolution(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if not (request.user.is_admin_user or request.user.is_staff_user):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ResolutionForm(request.POST)
        if form.is_valid():
            resolution = form.save(commit=False)
            resolution.complaint = complaint
            resolution.resolved_by = request.user
            resolution.save()

            new_status = form.cleaned_data.get('new_status')
            complaint.status = new_status
            complaint.save()

            # Notify complainant
            Notification.objects.create(
                user=complaint.submitted_by,
                complaint=complaint,
                title=f'Complaint {complaint.complaint_id} Updated',
                message=f'Your complaint "{complaint.title}" status has been updated to {complaint.get_status_display()}.'
            )

            messages.success(request, 'Resolution update added successfully.')

    return redirect('complaint_detail', pk=pk)


@login_required
def add_feedback(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if complaint.submitted_by != request.user:
        return HttpResponseForbidden()
    if complaint.status != 'resolved' or hasattr(complaint, 'feedback'):
        messages.error(request, 'Feedback cannot be submitted for this complaint.')
        return redirect('complaint_detail', pk=pk)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.complaint = complaint
            feedback.submitted_by = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')

    return redirect('complaint_detail', pk=pk)


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifs.filter(is_read=False).update(is_read=True)
    paginator = Paginator(notifs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'complaints/notifications.html', {'page_obj': page_obj})


@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'ok'})


@login_required
def admin_overview(request):
    if not request.user.is_admin_user:
        return HttpResponseForbidden()

    complaints_by_category = Category.objects.annotate(count=Count('complaints')).order_by('-count')
    complaints_by_status = {}
    for status, label in Complaint.STATUS_CHOICES:
        complaints_by_status[label] = Complaint.objects.filter(status=status).count()

    staff_members = User.objects.filter(role='staff')
    avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg']

    return render(request, 'complaints/admin_overview.html', {
        'complaints_by_category': complaints_by_category,
        'complaints_by_status': complaints_by_status,
        'staff_members': staff_members,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'total_feedback': Feedback.objects.count(),
    })


@login_required
def assign_complaint(request, pk):
    if not request.user.is_admin_user:
        return HttpResponseForbidden()
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        try:
            staff = User.objects.get(pk=staff_id, role='staff')
            complaint.assigned_to = staff
            complaint.status = 'under_review'
            complaint.save()
            Notification.objects.create(
                user=staff,
                complaint=complaint,
                title='Complaint Assigned to You',
                message=f'Complaint {complaint.complaint_id}: "{complaint.title}" has been assigned to you.'
            )
            Notification.objects.create(
                user=complaint.submitted_by,
                complaint=complaint,
                title='Your Complaint is Under Review',
                message=f'Your complaint "{complaint.title}" is now under review.'
            )
            messages.success(request, f'Complaint assigned to {staff.get_full_name()}.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid staff member selected.')
    return redirect('complaint_detail', pk=pk)
