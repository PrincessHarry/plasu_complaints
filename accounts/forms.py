from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    role = forms.ChoiceField(choices=[('student', 'Student'), ('staff', 'Staff')], widget=forms.Select())
    matric_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. PSU/2020/0001'}))
    staff_id = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Staff ID'}))
    department = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Department'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'matric_number', 'staff_id', 'department', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-input'})

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        matric_number = cleaned_data.get('matric_number')
        staff_id = cleaned_data.get('staff_id')

        if role == 'student' and not matric_number:
            self.add_error('matric_number', 'Matric number is required for students.')
        if role == 'staff' and not staff_id:
            self.add_error('staff_id', 'Staff ID is required for staff members.')
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-input'})
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', 'phone_number', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-input'})
