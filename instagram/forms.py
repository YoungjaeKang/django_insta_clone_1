from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['photo', 'caption', 'location']
        # 원래 caption이 charfield인데 widgets를 통해 Textarea로 수정 가능
        widgets = {
            'caption': forms.Textarea,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 2}),
        }
