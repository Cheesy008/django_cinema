from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'style': 'width:500px'}
            ),
        }
        labels = {
            'content': 'Введите текст сообщения',
        }



