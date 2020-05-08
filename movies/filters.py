import django_filters
from django import forms
from django.db.models import Avg
from django_filters.widgets import LookupChoiceWidget

from .models import Movie, Genre


class MovieFilter(django_filters.FilterSet):
    rating_choices = (
        ('ascending', 'По возрастанию'),
        ('descending', 'По убыванию'),
    )
    genre_choices = Genre.objects.values_list('pk', 'name')
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
        choices=genre_choices,
        label='ЖанрЫ',
        widget=forms.CheckboxSelectMultiple,
    )

    ordering = django_filters.ChoiceFilter(
        label='Сортировка по рейтингу',
        choices=rating_choices,
        method='filter_by_rating',
    )

    def filter_by_rating(self, queryset, name, value):
        m = Movie.objects.annotate(avg=Avg('rating__value'))
        expression = 'avg' if value == 'ascending' else '-avg'
        return m.order_by(expression)

    class Meta:
        model = Movie
        fields = (
            'genres',
            'category',
        )
