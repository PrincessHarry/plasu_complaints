from django import forms
from .models import Complaint, ComplaintAttachment, Feedback, Resolution, Category


DEFAULT_CATEGORIES = [
    {
        'name': 'Facilities & Infrastructure',
        'icon': 'building',
        'description': 'Issues with buildings, classrooms, toilets, water supply, electricity, etc.',
    },
    {
        'name': 'Academic Issues',
        'icon': 'book-open',
        'description': 'Exam irregularities, grading disputes, course content issues, academic integrity.',
    },
    {
        'name': 'Student Services',
        'icon': 'users',
        'description': 'Registration, transcripts, student welfare, counselling, and support services.',
    },
    {
        'name': 'Staff Conduct',
        'icon': 'user-x',
        'description': 'Unprofessional behaviour, misconduct, harassment, or discrimination by staff.',
    },
    {
        'name': 'Hostel & Accommodation',
        'icon': 'home',
        'description': 'Hostel conditions, allocation issues, maintenance, and security.',
    },
    {
        'name': 'Security & Safety',
        'icon': 'shield',
        'description': 'Campus security concerns, theft, unsafe conditions, emergency response.',
    },
    {
        'name': 'ICT & Technology',
        'icon': 'monitor',
        'description': 'Internet access, computer labs, portals, e-learning platforms.',
    },
    {
        'name': 'Health Services',
        'icon': 'heart',
        'description': 'Medical centre, health care quality, medications, and staff attitude.',
    },
    {
        'name': 'Library Services',
        'icon': 'book',
        'description': 'Library resources, opening hours, staff conduct, borrowing issues.',
    },
    {
        'name': 'Other',
        'icon': 'help-circle',
        'description': 'Any complaints not covered by other categories.',
    },
]


def get_active_categories():
    queryset = Category.objects.filter(is_active=True).order_by('name')
    if queryset.exists():
        return queryset

    # Bootstrap sensible defaults so category selects are never empty.
    for data in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=data['name'], defaults=data)

    return Category.objects.filter(is_active=True).order_by('name')


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'category', 'description', 'priority', 'location', 'is_anonymous']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Brief title of your complaint', 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the issue in detail. Include relevant dates, persons involved, and any previous attempts to resolve this...',
                'class': 'form-input',
                'rows': 6
            }),
            'priority': forms.Select(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Faculty of Science Building, Room 201', 'class': 'form-input'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = get_active_categories()
        self.fields['category'].empty_label = "Select a category"


class ComplaintFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All Statuses')] + list(Complaint.STATUS_CHOICES)
    PRIORITY_CHOICES = [('', 'All Priorities')] + list(Complaint.PRIORITY_CHOICES)

    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search complaints...', 'class': 'form-input'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-input'}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-input'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, empty_label='All Categories', widget=forms.Select(attrs={'class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = get_active_categories()


class FeedbackForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.HiddenInput(attrs={'id': 'rating-value'})
    )

    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Share your experience with the resolution process...',
                'class': 'form-input',
                'rows': 4
            }),
        }


class ResolutionForm(forms.ModelForm):
    new_status = forms.ChoiceField(choices=Complaint.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}))
    assign_to = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Resolution
        fields = ['notes', 'action_taken', 'is_public']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Update notes visible to the complainant...'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Internal notes on action taken...'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
