from django.db import models
from django.utils import timezone  # Import timezone for time-related fields
import datetime
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
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    exam_subject = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=80, choices=EXAM_TYPE_CHOICES)
    number_of_questions = models.IntegerField(default=0)
    time_setting = models.CharField(max_length=50, choices=TIME_SETTING_CHOICES)
    exam_time = models.TimeField(default=datetime.time(0, 0))
    visibility = models.CharField(max_length=50,choices=VISIBILITY_CHOICES,default="private")
    question_created = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam_name

class MCQQuestion(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)    

    def __str__(self):
        return self.question
    
class TrueFalseQuestion(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    correct_answer = models.BooleanField()    

    def __str__(self):
        return self.question
    
class ShortAnswerQuestion(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question = models.TextField()
    correct_answer = models.TextField()

    def __str__(self):
        return self.question