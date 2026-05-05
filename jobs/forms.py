# jobs/forms.py ← CREATE this file
from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model  = JobApplication
        fields = ['company', 'role', 'salary', 'status', 'notes']
        # owner aur date_applied nahi — woh automatically set hote hain

        widgets = {
            'company': forms.TextInput(attrs={
                'placeholder': 'Company ka naam',
                'style': 'width:100%; padding:10px; border:1px solid #ddd; border-radius:4px;'
            }),
            'role': forms.TextInput(attrs={
                'placeholder': 'Job role',
                'style': 'width:100%; padding:10px; border:1px solid #ddd; border-radius:4px;'
            }),
            'salary': forms.NumberInput(attrs={
                'placeholder': 'Expected salary',
                'style': 'width:100%; padding:10px; border:1px solid #ddd; border-radius:4px;'
            }),
            'status': forms.Select(attrs={
                'style': 'width:100%; padding:10px; border:1px solid #ddd; border-radius:4px;'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Koi notes...',
                'style': 'width:100%; padding:10px; border:1px solid #ddd; border-radius:4px;'
            }),
        }