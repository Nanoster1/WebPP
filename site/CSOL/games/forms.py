from django import forms

from .models import Comment


class CommentForm(forms.Form):

    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )

    comment_area = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Ваш текст'})
    )