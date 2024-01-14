from django.db import models


class Course(models.Model):
    name_course = models.CharField(max_length=100, verbose_name='Наименование Курса')
    picture = models.ImageField(upload_to='course/', verbose_name='Картинка', blank=True, null=True)
    description = models.CharField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return f'{self.name_course}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('name_course',)

class Lesson(models.Model):
    name_course = models.CharField(max_length=100, verbose_name='Наименование Урока')
    description = models.CharField(max_length=500, verbose_name='Описание')
    picture = models.ImageField(upload_to='lesson/', verbose_name='Картинка', blank=True, null=True)
    url_video = models.CharField(max_length=200, verbose_name='Ссылка на видео')

    def __str__(self):
        return f'{self.name_course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('name_course',)