from rest_framework import viewsets, generics
from training.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscribeSerializer
from training.models import Course, Lesson, Payments, Subscribe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsUser, IsModerator
from training.paginations import LessonPagination
from requests import Response
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from datetime import datetime
from training.services import *


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator, IsUser]
    pagination_class = LessonPagination

    def partial_update(self, request, pk=None):
        course = self.get_object()
        course.date_update = datetime.now()
        course.save(update_fields=['date_update'])
        serializer = self.get_serializer(course)
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.role == "member":
            return Course.objects.filter(user=self.request.user)
        elif self.request.user.role == 'moderator':
            return Course.objects.all()

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsUser]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsUser, IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsModerator, IsUser]
        return [permission() for permission in permission_classes]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LessonPagination


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson')
    ordering_fields = ('payment_date',)


# class PaymentsCreateAPIView(generics.CreateAPIView):
#     serializer_class = PaymentsSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permission_classes = [AllowAny]

    # permission_classes = [IsAuthenticated, IsUser]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    payment_service = PaymentService()

    def perform_create(self, serializer):
        payment_intent = self.payment_service.create_payment_intent()

        new_payment = serializer.save(
            user=self.request.user,
            session_id=payment_intent.id,
            amount=payment_intent.amount
        )


class GetPaymentView(APIView):

    def get(self, request, payment_id):
        payment_intent = get_payment(payment_id)
        return Response({'status': payment_intent.status, 'body': str(payment_intent)})



#

class SubscribeCreateAPIView(generics.CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    # # Создаем и сохраняем подписку
    # def perform_create(self, serializer, *args, **kwargs):
    #     subscribe = serializer.save()  # получаем данные подписки
    #     subscribe.user = self.request.user  # сохраняем данные о подписке в профиль пользователя
    #     course_pk = self.kwargs.get('pk')  # сохраняем данные о подписке в профиль курс
    #     subscribe.course = Course.objects.get(pk=course_pk)  # получаем нужную подписку
    #     subscribe.save()


class SubscribeDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer



class SubscribeListAPIView(generics.ListAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer



class SubscribeUpdateAPIView(generics.UpdateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
