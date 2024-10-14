from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, permissions, status
from django.db.models import Q
from django.utils.timezone import now
from rest_framework.response import Response


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

    def post(self, request, pk):
        task = Task.objects.get(pk=pk, owner=request.user)
        task.is_completed = not task.is_completed
        task.save()
        
        return Response({'status': 'task_completion_toggled'}, status=status.HTTP_200_OK)

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







# Create your views here.
