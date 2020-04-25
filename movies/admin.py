from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms

from .models import (
    Movie,
    RatingStar,
    Rating,
    Category,
    Genre,
    MoviePerson,
    MovieShots,
)
from reviews.models import Review


class ReviewInline(GenericTabularInline):
    model = Review
    extra = 1


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1


@admin.register(MoviePerson)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birthday_date', 'get_image')

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='100px' height='100' />")

    get_image.short_description = 'Изображение'


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    prepopulated_fields = {'url': ('title',)}
    inlines = [ReviewInline, MovieShotsInline]


admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(MovieShots)
