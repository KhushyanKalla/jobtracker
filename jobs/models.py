from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobApplication(models.Model):
    
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('offer', 'Offer'),
    ]
        
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=150)
    salary = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )
    date_applied = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_application'
    )
    
    def __str__(self):
        return f"{self.role} at {self.company}"