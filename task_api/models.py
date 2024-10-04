from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    priority_level = models.CharField(
        max_length=6,
        choices = PRIORITY_CHOICES,
        default=MEDIUM,
    )

    PENDING = 'Pending'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed')
    ]
    status = models.CharField(
        max_length=10,
        choices = STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return self.title

# Create your models here.
