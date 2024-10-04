from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks-detail/', TaskDetailView.as_view(), name='task-detail'),
]