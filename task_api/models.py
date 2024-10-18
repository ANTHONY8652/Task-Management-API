from django.db import models
from users.models import User
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
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

    WORK = 'Work'
    PERSONAL = 'Personal'
    UNSURE = 'Unsure'
    HEALTH = 'Health'
    FINANCE = 'Finance'
    HOBBY = 'Hobby'
    URGENT = 'Urgent'
    LEARNING = 'Learning'
    SOCIAL = 'Social'

    CATEGORY_CHOICES = [
        (WORK, 'Work'),
        (PERSONAL, 'Personal'),
        (UNSURE, 'Unsure'),
        (HEALTH, 'Health'),
        (FINANCE, 'Finance'),
        (HOBBY, 'Hobby'),
        (URGENT, 'Urgent'),
        (LEARNING, 'Learning'),
        (SOCIAL, 'Social'),
        ]
    category = models.CharField(
        max_length = 20,
        choices = CATEGORY_CHOICES,
        default = UNSURE
    )

    RECURRING_CHOICES = [
        ('none', 'No Recurrence'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    recurrence_type = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none')
    next_due_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_completed and self.recurrence_type != 'none':
            self.set_next_due_date()
            self.is_completed = False
        super().save(*args, **kwargs)

    def set_next_due_date(self):
        if self.recurrence_type == 'daily':
            self.next_due_date = timezone.now() + timedelta(days=1)
        elif self.recurrence_type == 'weekly':
            self.next_due_date = timezone.now() + timedelta(weeks=1)
        elif self.recurrence_type == 'monthly':
            self.next_due_date = timezone.now() + timedelta(weeks=4)
        elif self.recurrence_type == 'yearly':
            self.next_due_date = timezone.now() + timedelta(weeks=52)

        self.due_date = self.next_due_date

    def mark_completed(self):
        #Mark the tast as completed and store the time.
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save
    
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = 'shared_tasks',
        blank = True
    )

    def __str__(self):
        return f'{self.owner} created {self.title} task on {self.created_at}'

# Create your models here.
