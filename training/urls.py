from training.apps import TrainingConfig
from rest_framework.routers import DefaultRouter
from training.views import (LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                            LessonUpdateAPIView, LessonDestroyAPIView, PaymentsCreateAPIView, CourseViewSet,
                            PaymentsListAPIView, SubscribeViewSet, GetPaymentView, PaymentsCreateApiView, SubscribeCreateAPIView,
                            SubscribeDestroyAPIView, SubscribeListAPIView, SubscribeUpdateAPIView)
from django.urls import path, include


app_name = TrainingConfig.name

router = DefaultRouter()
router.register(r'trainings', CourseViewSet, basename='trainings')
router.register(r'subscribe', SubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-Retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-Update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments-create'),
    path('course/', CourseViewSet.as_view({'get': 'list'}), name='course-view'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path('payments/create/', PaymentsCreateApiView.as_view(), name='payments-create'),
    path('payments/<str:payment_id>/', GetPaymentView.as_view(), name='payment_get'),
    path('lesson/subscribe/', include(router.urls)),

    path("subscribe/", SubscribeListAPIView.as_view(), name="subscribe_list"),
    path('subscribe/<int:pk>/', SubscribeCreateAPIView.as_view(), name='subscribe-create'),
    path('subscribe/delete/<int:pk>/', SubscribeDestroyAPIView.as_view(), name='subscribe-delete'),
    path("subscribe/update/<int:pk>/", SubscribeUpdateAPIView.as_view(), name="subscribe_update"),
        ] + router.urls
