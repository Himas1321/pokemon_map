from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100)
    title_jp = models.CharField(max_length=100, blank=True, null=True)
    title_en = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to="pokemon",blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    attack = models.IntegerField(default=5)
    defence = models.IntegerField(default=10)
    stamina = models.IntegerField(default=100)