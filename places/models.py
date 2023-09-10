from django.db import models


class PlaceName(models.Model):
    title = models.CharField('Заголовок', max_length=128)
    short_description = models.TextField('Короткое описание', blank=True)
    long_description = models.TextField('Полное описание', blank=True)
    longitude = models.FloatField('Долгота точки', blank=True)
    latitude = models.FloatField('Широта точки', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PlaceImage(models.Model):
    numb = models.IntegerField("Порядковый номер:", db_index=True, default=0, blank=True)
    place = models.ForeignKey(PlaceName, on_delete=models.CASCADE, verbose_name="Место", related_name='pictures')
    picture = models.ImageField("Картинка", upload_to='img')

    def __str__(self):
        return f'{self.numb} {self.place}'

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
        ordering = ['numb']




