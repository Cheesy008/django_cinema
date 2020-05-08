from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from reviews.models import Review
from .filters import MovieFilter
from .mixins import ObjectDetailMixin
from .models import (
    Movie,
    MoviePerson,
    Rating,
)
from reviews.forms import ReviewForm
from .forms import RatingForm


class IndexView(ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['filter'] = MovieFilter(self.request.GET, queryset=self.queryset)
        return context


class MoviePersonListView(ListView):
    model = MoviePerson
    template_name = 'movies/movie_person_list.html'
    context_object_name = 'persons'


class MovieDetailView(ObjectDetailMixin, FormMixin, DetailView):
    form_class = ReviewForm
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    lookup = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.kwargs.get('')).prefetch_related('movieshots').only('movieshots__image')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = Movie.objects.get(url=self.kwargs['slug'])
        context['reviews'] = Review.objects.filter(movie__url=self.kwargs['slug'])
        context['rating_form'] = RatingForm()
        try:
            context['your_rating'] = Rating.objects.get(user=self.request.user, movie=movie)
        except Rating.DoesNotExist:
            context['your_rating'] = None
        return context


class MoviePersonView(ObjectDetailMixin, FormMixin, DetailView):
    form_class = ReviewForm
    model = MoviePerson
    template_name = 'movies/movie_person_detail.html'
    context_object_name = 'person'
    lookup = 'pk'


class SearchView(View):
    def get(self, request):
        movies = Movie.objects.all()
        query = request.GET.get('search')

        if query:
            movies = movies.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(title__iexact=query) |
                Q(description__iexact=query)
            ).distinct()
        context = {'searched_movies': movies}
        return render(request, 'movies/search_results.html', context)


class AddRating(View):
    def post(self, request):
        form = RatingForm(request.POST or None)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=self.request.user,
                movie_id=int(request.POST.get('movie')),
                defaults={'value': request.POST.get('value')},
            )
            return HttpResponse(status=201)
        return HttpResponse(status=400)
