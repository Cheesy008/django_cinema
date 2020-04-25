import django_filters
from django import forms
from django_filters.widgets import LookupChoiceWidget

from .models import Movie, Genre


class MovieFilter(django_filters.FilterSet):
    choices = Genre.objects.values_list('pk', 'name')
    year__gt = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='gt',
        label='Год',
        widget=forms.TextInput(attrs={
            'placeholder': 'от'
        })
    )
    year__lt = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='lt',
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'до'
        })
    )
    genres = django_filters.MultipleChoiceFilter(
        choices=choices,
        label='ЖанрЫ',
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Movie
        fields = (
            'genres',
            'category',
        )
