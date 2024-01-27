from rest_framework import serializers
from training.models import Course, Lesson, Payments


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
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    class Meta:
        model = Course
        fields = '__all__'
        #fields = ['name_course','description','payments','lesson_count','lessons']

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    # def create(self, validated_data):
    #     payments_data = validated_data.pop('payments')
    #
    #     course_item = Course.objects.create(**validated_data)
    #
    #     for payment_data in payments_data:
    #         Payments.objects.create(**payment_data, course=course_item)
    #
    #     return course_item