from django.contrib import admin

from .models import Movie, Actor, MovieActor, MovieGenre


class MovieActorInline(admin.StackedInline):
    model = MovieActor
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year')
    list_filter = ('year', 'genre')
    inlines = [MovieActorInline]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    inlines = [MovieActorInline]


@admin.register(MovieActor)
class MovieActorAdmin(admin.ModelAdmin):
    pass


@admin.register(MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
    pass
