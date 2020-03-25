from django.db import models

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название RU')
    title_en = models.CharField(max_length=200, default='', blank=True, verbose_name='Название EN')
    title_jp = models.CharField(max_length=200, default='', blank=True, verbose_name='Название JP')
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.PROTECT, verbose_name='Покемон', related_name='pokemon_entities')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время исчезновения')
    level = models.IntegerField(blank=True, null=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True, null=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, null=True, verbose_name='Атака')
    defence = models.IntegerField(blank=True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon}'