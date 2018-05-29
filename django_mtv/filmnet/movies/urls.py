from django.urls import path

from movies.views import (
    movies_list,
    movie_detail,
)

urlpatterns = [
    path(
        '',
        movies_list,
        name='movies_list'
    ),
    path(
        '<int:movie_id>/',
        movie_detail,
        name='movie_detail'
    ),
]
