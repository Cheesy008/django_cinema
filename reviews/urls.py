from django.urls import path
from .views import movie_review

app_name = 'reviews'


urlpatterns = [
    path('movie-comment/<slug:slug>/', movie_review, name='movie_review'),
    path('movie-comment/<slug:slug>/<int:parent_comment_id>', movie_review, name='comment_reply'),
]