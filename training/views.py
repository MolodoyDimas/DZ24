from django.shortcuts import render
from rest_framework import viewsets
from training.serializers import CourseSerializer
from training.models import Course

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()