from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, permissions, status
from django.db.models import Q
from django.utils.timezone import now
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

##Task CRUD operations
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class TaskToggleCompleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    """"
    def post(self, request, pk):
        task = Task.objects.get(pk=pk, owner=request.user)
        task.is_completed = not task.is_completed
        task.save()
        
        return Response({'status': 'task_completion_toggled'}, status=status.HTTP_200_OK)
    """
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return Response(TaskSerializer(task).data)
    

class UserTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

class TaskSearchView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q')
        return Task.objects.filter(owner=self.request.user).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

class TaskPriorityUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        task = self.get_object()
        task.priority = request.data.get('priority', task.priority)
        task.save()
        
        return Response({'status': 'priority updated'}, status=status.HTTP_200_OK)
    
class OverdueTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user, due_date__lt=now, is_completed=False)

class TaskCompleteView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        task.mark_completed()
        
        return Response({
            'detail': 'Task marked as completed',
            'task': TaskSerializer(task).data
        }, status=status.HTTP_200_ok)

class CompletedTaskListView(generics.ListAPIView):
    serializer_class = Task
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objecs.filter(is_completed=True).order_by('-completed_at')

class ShareTaskView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        user_ids = request.data.get('user_ids', [])
        users = User.objects.filter(id__in=user_ids)

        task.shared_with.set(users)
        task.save()

        return Response({
            'detail': 'Task shared successfully',
            'task': TaskSerializer(task).data
        }, status=status.HTTP_200_OK)

class SharedTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(shared_with=self.request.user).order_by('-id')


# Create your views here.
