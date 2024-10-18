from django.urls import path
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskToggleCompleteView,
    UserTaskListView,
    TaskSearchView,
    TaskPriorityUpdateView,
    OverdueTasksView, TaskCompleteView, 
    CompletedTaskListView, SharedTaskListView, 
    ShareTaskView,
)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/toggle-complete/', TaskToggleCompleteView.as_view(), name='task-toggle-complete'),
    path('my-tasks/', UserTaskListView.as_view(), name='user-task-list'),
    path('search-tasks/', TaskSearchView.as_view(), name='task-search'),
    path('tasks/<int:pk>/update-priority/', TaskPriorityUpdateView.as_view(), name='task-priority-update'),
    path('overdue-tasks/', OverdueTasksView.as_view(), name='overdue-tasks'),
    path('tasks/<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
    path('task/completed/', CompletedTaskListView.as_view(), name='completed-task-list'),
    path('tasks/<int:pk>/share/', ShareTaskView.as_view(), name='share-task'),
    path('tasks/shared/', SharedTaskListView.as_view(), name='shared-task-list'),
]