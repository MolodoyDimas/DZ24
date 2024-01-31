import pytz
from celery import shared_task
from models import Course, Subscribe
from users.models import User
import datetime

@shared_task
def check_update(pk):
    course = Course.objects.get(pk=pk)

    subscriptions = Subscribe.objects.filter(course=pk)

    if subscriptions:
        for subscription in subscriptions:
            print(f'Привет, {subscription.user}! Автор курса "{course.course_title}" внёс изминения!')


@shared_task
def check_user_activity():
    users = User.objects.all()

    moscow_timezone = pytz.timezone('Europe/Moscow')
    current_date = datetime.datetime.now()
    current_tz = current_date.astimezone(moscow_timezone)

    for user in users:
        if user.last_login:
            user_last_login = user.last_login.astimezone(moscow_timezone)

            if (current_tz.date() - user_last_login.date()).days > 30:
                user.is_active = False
                user.save()
        else:
            user.last_login = current_tz
            user.save()