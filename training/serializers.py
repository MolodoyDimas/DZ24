from rest_framework import serializers
from training.models import Course, Lesson, Payments


class Meta:
    model = Course
    fields = '__all__'


def get_lesson_count(self, obj):
    return obj.lesson_set.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set')


class CourseCreateSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        payments = validated_data.pop('payments')

        course_item = Course.objects.create(**validated_data)

        for x in payments:
            Payments.objects.create(**x, course=course_item)

        return course_item
