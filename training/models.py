from django.db import models
from users.models import User
from config.settings import AUTH_USER_MODEL
import stripe

class Course(models.Model):
    name_course = models.CharField(max_length=100, verbose_name='Наименование Курса')
    picture = models.ImageField(upload_to='course/', verbose_name='Картинка', blank=True, null=True)
    description = models.CharField(max_length=500, verbose_name='Описание')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Создатель')

    def __str__(self):
        return f'{self.name_course}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('name_course',)


class Lesson(models.Model):
    name_lesson = models.CharField(max_length=100, verbose_name='Наименование Урока')
    description = models.CharField(max_length=500, verbose_name='Описание')
    picture = models.ImageField(upload_to='lesson/', verbose_name='Картинка', blank=True, null=True)
    url_video = models.CharField(max_length=200, verbose_name='Ссылка на видео')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Создатель')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', blank=True, null=True)

    def __str__(self):
        return f'{self.name_lesson}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('name_lesson',)


class Payments(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_date = models.PositiveIntegerField(verbose_name='Дата платежа', null=True, blank=True)
    amount = models.IntegerField(default=0, verbose_name='Сумма оплаты')
    method = models.BooleanField(default=True, verbose_name='Оплата переводом')  # если наличные - False

    is_paid = models.BooleanField(default=False, verbose_name='статус оплаты')
    session_id = models.CharField(max_length=150, verbose_name='id сессии', null=True, blank=True)

    def __str__(self):
        return f"{self.course if self.course else self.lesson} - {self.amount}"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ('user',)

class Subscribe(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Активность подписки')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', null=True, blank=True)

    def __str__(self):
        return f'{self.is_active}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'