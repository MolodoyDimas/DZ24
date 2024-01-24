from django.shortcuts import render
from rest_framework import viewsets, generics
from training.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, CourseCreateSerializer
from training.models import Course, Lesson, Payments


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializer