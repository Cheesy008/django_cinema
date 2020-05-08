from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from movies.models import Movie
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
)


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    serializer_action_classes = {
        'list': MovieListSerializer,
        'retrieve': MovieDetailSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()



