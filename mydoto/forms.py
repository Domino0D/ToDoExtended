from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm): # Form to change private state
    class Meta:
        model = Profile
        fields = ['is_private']