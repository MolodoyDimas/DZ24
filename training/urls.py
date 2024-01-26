from training.apps import TrainingConfig
from rest_framework.routers import DefaultRouter
from training.views import (LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                            LessonUpdateAPIView, LessonDestroyAPIView, PaymentsCreateAPIView, CourseViewSet,
                            PaymentsListAPIView)
from django.urls import path


app_name = TrainingConfig.name

router = DefaultRouter()
router.register(r'trainings', CourseViewSet, basename='trainings')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-Retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-Update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments-create'),
    path('course/', CourseViewSet.as_view({'get': 'list'}), name='course-view'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
        ] + router.urls
