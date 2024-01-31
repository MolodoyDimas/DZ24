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


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator, IsUser]
    pagination_class = LessonPagination

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


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permission_classes = [AllowAny]

    # permission_classes = [IsAuthenticated, IsUser]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class PaymentsCreateApiView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_payment = serializer.save()
        stripe.api_key = 'pk_test_51OeDbXASb9i3kG2Vf4PrZ0b27t8CuJDWmGZ5NsjSr0vaRaJsMxndyH8msKKRYM9tEXJGvvscHjPTZvBJKdKxG3QP00vR0gmc1o'
        payment_intent = stripe.PaymentIntent.create(
            amount=2000,
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        new_payment.session_id = payment_intent.id
        new_payment.amount = payment_intent.amount
        new_payment.save()

        return super().perform_create(new_payment)


class GetPaymentView(APIView):

    def get(self, request, payment_id):
        payment = Payments.objects.get(pk=payment_id)
        payment_id = payment.session_id
        stripe.api_key = 'sk_test_51OdoXSHC8LUh8NqZQboynIwfP7znL7qfNqCOqOYkl7k3pzAKN8QU45ye5RpnABJ2MRjLBfk6tWWisTmY9QoiXJNR00NP3ImbNV'
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        print(payment_intent)
        return Response({'status': payment_intent.status, 'body': payment_intent})
