from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment # form과 model 연결
        fields = ['contents'] 
        widgets = {
            'contents': forms.Textarea(attrs={'placeholder': 'Enter your comment here'}),
        }