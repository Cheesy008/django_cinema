from django import template

from movies.filters import MovieFilter
from movies.models import Category, Movie


register = template.Library()


@register.inclusion_tag('movies/includes/latest_movies.html')
def get_latest_movies(count=3):
    latest_movies = Movie.objects.only(
        'title',
        'thumbnail',
        'url',
    ).order_by('-created')[:count]
    return {'latest_movies': latest_movies}

