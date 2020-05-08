from django import forms

from .models import Rating


class RatingForm(forms.ModelForm):
    value = forms.ChoiceField(
        choices=Rating.Value.choices,
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = Rating
        fields = ('value',)
