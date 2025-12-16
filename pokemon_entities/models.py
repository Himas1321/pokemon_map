from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    description = models.TextField(
        'Описание', blank=True, null=True
    )
    title = models.CharField('Имя', max_length=100)
    title_jp = models.CharField(
        'Японское имя', max_length=100, blank=True, null=True
    )
    title_en = models.CharField(
        'Английское имя', max_length=100, blank=True, null=True
    )
    photo = models.ImageField(
        'Фотография', upload_to="pokemon",blank=True, null=True
    )
    previous_evolution = models.ForeignKey(
        "self", on_delete=models.SET_NULL,
        blank=True, null=True, related_name="next_evolution", 
        verbose_name='Эволюция'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, verbose_name='Покемон',
    )
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Дата появления', default=timezone.now)
    disappeared_at = models.DateTimeField('Дата исчезновения', blank=True, null=True)
    level = models.IntegerField('Уровень', default=1)
    health = models.IntegerField('Здоровье', default=100)
    attack = models.IntegerField('Атака', default=5)
    defence = models.IntegerField('Защита', default=10)
    stamina = models.IntegerField('Выносливость', default=100)