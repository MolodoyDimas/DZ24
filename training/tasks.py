from django.conf import settings
from django.core.mail import send_mail

from training.models import Course


def check_update():
    recipient_email = 'www.rufat@bk.ru'
    for i in Course.objects.all():
        if i.date_update > i.date_preview:
            send_mail(
                subject='Информация о курсе',
                message=f'Курс был обновлен',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email]

            )
    return len(i)