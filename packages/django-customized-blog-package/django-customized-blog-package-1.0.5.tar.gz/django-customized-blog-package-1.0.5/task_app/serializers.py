from rest_framework import serializers
from .models import TaskQueue


class TaskQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskQueue
        fields = '__all__'


