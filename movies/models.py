from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=150
    )
    description = models.TextField('Описание')
    url = models.SlugField(
        max_length=150,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=150
    )
    description = models.TextField('Описание')
    url = models.SlugField(
        max_length=150,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class MoviePerson(models.Model):

    class PersonGender(models.TextChoices):
        MALE = 'MA', 'Мужчина'
        FEMALE = 'FE', 'Женщина'

    name = models.CharField(
        'Имя',
        max_length=150
    )
    gender = models.CharField(
        verbose_name='Пол',
        max_length=2,
        choices=PersonGender.choices,
        default=PersonGender.MALE,
    )
    biography = models.TextField(verbose_name='Биография')
    birthday_date = models.PositiveIntegerField(
        verbose_name='Дата рождения',
        default=0,
    )
    height = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Рост',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='movie_persons/'
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='person_genres',
        blank=True,
    )
    as_producer = models.ManyToManyField(
        'Movie',
        verbose_name='Как продюсер',
        related_name='as_movie_producer',
        blank=True,
    )
    as_scenarist = models.ManyToManyField(
        'Movie',
        verbose_name='Как сценарист',
        related_name='as_movie_scenarist',
        blank=True,
    )
    as_actor = models.ManyToManyField(
        'Movie',
        verbose_name='Как актёр',
        related_name='as_movie_actor',
        blank=True,
    )
    as_director = models.ManyToManyField(
        'Movie',
        verbose_name='Как режиссёр',
        related_name='as_movie_director',
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('movies:movie_person', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Участник кино'
        verbose_name_plural = 'Участники кино'


class Movie(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )
    tagline = models.CharField(
        'Слоган',
        max_length=150
    )
    description = models.TextField(
        'Описание',
    )
    thumbnail = models.ImageField(
        upload_to='movie_thumbnail/',
        null=True,
        blank=True,
    )
    year = models.PositiveIntegerField(
        'Год выхода',
        default=0
    )
    created = models.DateTimeField(
        'Добавлен на сайт',
        auto_now_add=True,
        null=True,
        blank=True
    )
    country = models.CharField(
        'Страна',
        max_length=150
    )
    actors = models.ManyToManyField(
        MoviePerson,
        verbose_name='Актёры',
        related_name='film_actors',
        blank=True,
    )
    directors = models.ManyToManyField(
        MoviePerson,
        verbose_name='Режиссёры',
        related_name='film_directors',
        blank=True,
    )
    scenarists = models.ManyToManyField(
        MoviePerson,
        verbose_name='Сценаристы',
        related_name='film_scenarists',
        blank=True,
    )
    producers = models.ManyToManyField(
        MoviePerson,
        verbose_name='Продюсеры',
        related_name='film_producers',
        blank=True,
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='film_genres',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='film_category'
    )
    budget = models.PositiveIntegerField(
        'Бюджет',
        default=0
    )
    fees_in_usa = models.PositiveIntegerField(
        'Сборы в США',
        default=0
    )
    fees_in_world = models.PositiveIntegerField(
        'Сборы в мире',
        default=0
    )
    url = models.SlugField(
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('movies:movie_detail', kwargs={'slug': self.url})

    @property
    def average_rating(self):
        return Rating.objects.filter(movie=self).aggregate(avg=Avg('value'))

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )
    description = models.TextField('Описание')
    image = models.ImageField(
        'Изображение',
        upload_to='movie_shots/'
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name='Фильм',
        on_delete=models.CASCADE,
        related_name='movieshots_movie'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class Rating(models.Model):
    class Value(models.IntegerChoices):
        EXCELLENT = 5
        VERY_GOOD = 4
        GOOD = 3
        AVERAGE = 2
        POOR = 1

    value = models.PositiveSmallIntegerField(
        choices=Value.choices,
        default=Value.POOR,
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name='Фильм',
        on_delete=models.CASCADE,
        related_name='rating',
    )

    def __str__(self):
        return f"{self.movie.title} - {self.value}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
