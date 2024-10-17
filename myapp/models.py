from django.db import models
from django.utils import timezone  # Import timezone for time-related fields

# Custom User Model
class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128, default="")
    email = models.EmailField(unique=True)  # Add unique constraint to email
    mobile = models.PositiveBigIntegerField()
    address = models.TextField(default="")
    city = models.CharField(max_length=100,default="")
    country = models.CharField(max_length=100,default="")
    is_login = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)  # Use timezone.now
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_login:
            self.last_login = timezone.now()  # Update last_login with current time
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name


# Exam Model
class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Questions'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
        ('MX', 'Mix'),
    ]
    TIME_SETTING_CHOICES = [
        ('exam', 'Full Exam Time'),
        ('question', 'Single Question Time'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    exam_subject = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=80, choices=EXAM_TYPE_CHOICES)
    number_of_questions = models.PositiveBigIntegerField()
    time_setting = models.CharField(max_length=50, choices=TIME_SETTING_CHOICES)
    exam_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam_name
