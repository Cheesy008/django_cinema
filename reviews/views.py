from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from movies.models import Movie
from .forms import ReviewForm
from .models import Review


def movie_review(request, slug, parent_comment_id=None):
    movie = get_object_or_404(Movie, url=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        print(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.content_type = form.cleaned_data.get('content_type')
            new_review.object_id = form.cleaned_data.get('object_id')
            new_review.content = form.cleaned_data.get('content')
            new_review.user = request.user
            if parent_comment_id:
                parent_comment = Review.objects.get(id=parent_comment_id)
                new_review.parent_id = parent_comment.get_root().id
                new_review.reply_to = parent_comment.user
                new_review.save()
                return redirect(movie)
            new_review.save()
            return redirect(movie)
        else:
            messages.add_message(request, messages.WARNING, 'Форма заполнена неверно')
            return redirect(movie)
    else:
        initial_data = {
            'content_type': movie.get_content_type,
            'object_id': movie.id,
        }
        form = ReviewForm(initial=initial_data)
        print(request.POST)
        context = {
            'form': form,
            'slug': slug,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'reviews/reply.html', context)
