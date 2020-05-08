from django.urls import path

from .views import(
    IndexView,
    MovieDetailView,
    MoviePersonView,
    SearchView,
    AddRating,
    MoviePersonListView,
)

app_name = 'movies'

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('name/<int:pk>/', MoviePersonView.as_view(), name='movie_person'),
    path('movie/<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('rating/', AddRating.as_view(), name='add_rating'),
    path('person_list/', MoviePersonListView.as_view(), name='person_list'),
    path('', IndexView.as_view(), name='index'),
]