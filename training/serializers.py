from rest_framework import serializers
from training.models import Course, Lesson, Payments, Subscribe
from training.validators import LinkValidator

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(fields='link_video')]

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"

class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    subscribe = SubscribeSerializer(source='subscribe_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def get_subscribe(self, obj):
        return obj.subscribe_set.all()