from rest_framework import serializers

from devboard.models import Comment, Task


class CommentSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'body', 'created']
        read_only_fields = ['id', 'author_name', 'created']

class TaskSerializer(serializers.ModelSerializer):

    assignee_name = serializers.CharField(source='assignee.username', read_only=True)

    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'assignee_name', 'project_name']

#            'id', 'author_name', 'title', 'description']
        read_only_fields = ['id', 'created_at']

