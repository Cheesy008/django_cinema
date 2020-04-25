from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .filters import MovieFilter
from .mixins import ObjectDetailMixin
from .models import (
    Movie,
    MoviePerson,
)
from reviews.forms import ReviewForm


class IndexView(ListView):
    model = Movie
    queryset = Movie.objects.only(
        'title',
        'thumbnail',
        'tagline',
        'url',
    )
    template_name = 'movies/index.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['filter'] = MovieFilter(self.request.GET, queryset=self.queryset)
        return context


class MovieDetailView(ObjectDetailMixin, FormMixin, DetailView):
    form_class = ReviewForm
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    lookup = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.kwargs.get('')).prefetch_related('movieshots').only('movieshots__image')


class MoviePersonView(ObjectDetailMixin, FormMixin, DetailView):
    form_class = ReviewForm
    model = MoviePerson
    template_name = 'movies/movie_person.html'
    context_object_name = 'person'
    lookup = 'pk'


class SearchView(View):
    def get(self, request):
        movies = Movie.objects.all()
        query = request.GET.get('search')

        if query:
            movies = movies.filter(
                Q(title__icontains=query) |
                Q(description__contains=query)
            ).distinct()
        context = {'searched_movies': movies}
        return render(request, 'movies/search_results.html', context)




