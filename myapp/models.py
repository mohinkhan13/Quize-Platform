from django.db import models

# Create your models here.
class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField()
    mobile = models.PositiveBigIntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_login = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_login:  # Check if is_login is True
            self.last_login = timezone.now()  # Update last_login with current time
        super().save(*args, **kwargs)  # Call the parent save method

    def __str__(self):
        return self.first_name
    

class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ("MCQ","MCQ"),
        ("TF","TF"),
        ("SA","SA"),
        ("MCQ","MCQ"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    exam_subject = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=80, choices=EXAM_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam_name