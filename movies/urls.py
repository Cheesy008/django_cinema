from django.urls import path

from .views import(
    IndexView,
    MovieDetailView,
    MoviePersonView,
    SearchView,
)

app_name = 'movies'

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('', IndexView.as_view(), name='index'),
    path('name/<int:pk>/', MoviePersonView.as_view(), name='movie_person'),
    path('movie/<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
]