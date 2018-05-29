from django.http import Http404
from django.shortcuts import render, redirect

from movies.models import Movie, MovieActor


def movies_list(request):
    movies = Movie.objects.all()

    return render(
        request,
        'movies/list.html',
        {
            'movies': movies,
        }
    )


def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return redirect('/movies')

    return render(
        request,
        'movies/detail.html',
        {
            'movie': movie,
        }
    )
