from rest_framework import serializers
from .models import Task
from django.core.exceptions import ValidationError

class TaskSerializer(serializers.ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'due_date', 'owner', 'is_completed', 'completed_at', 'shared_with']
        read_only_fields = ['created_at', 'owner']

        def validate(self, data):
            task = Task(**data)

            try:
                task.clean()
            
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
            
            return data
        
        def create(self, validated_data):
            title = validated_data.pop('title').strip().lower()

            validated_data['owner'] = self.context['request'].user

            task = Task.objects.create(title=title, **validated_data)

            return task