from django import forms
from .models import Post, Comment

class Post_form(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'img']

class Comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['comment_text']

        widgets ={
            'comment_text': forms.Textarea(attrs={'rows':3}),
        }

        labels = {
            'comment_text': '',
        }