from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="pokemon",blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()