from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'content',
            'content_type',
            'object_id'
        )
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'content': forms.Textarea(
                attrs={'style': 'width:500px'}
            ),
        }
        labels = {
            'content': 'Введите текст сообщения',
        }



