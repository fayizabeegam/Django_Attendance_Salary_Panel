from django.db import models

# Create your models here.

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('Accounts', 'Accounts'),
        ('Attendance', 'Attendance'),
        ('HR Conversion', 'HR Conversion'),
        ('Employee Info', 'Employee Info'),
    ]

    Date = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    Model = models.CharField(max_length=50, choices=ACTION_CHOICES)
    Action = models.CharField(max_length=100)
    Content = models.TextField()

    def __str__(self):
        return f"{self.Date} - {self.User.username} - {self.Action}"

