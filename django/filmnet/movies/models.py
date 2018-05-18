from django.db import models


class MovieGenre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=1000)
    genre = models.ForeignKey(
        MovieGenre,
        on_delete=models.CASCADE,
    )
    year = models.IntegerField()

    def __str__(self):
        return self.title


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name,
        )


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(
            str(self.actor),
            str(self.movie),
        )
