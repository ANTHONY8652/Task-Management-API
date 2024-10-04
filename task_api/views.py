from .models import Task
from rest_framework import generics, serializers
from .serializers import TaskSerializer


##Task CRUD operations
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
# Create your views here.
