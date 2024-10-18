from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Agency(models.Model):
    ORGANIZATION_TYPE_CHOICES = [
        ('NGO', 'Non-Governmental Organization'),
        ('GOV', 'Government'),
        ('PRV', 'Private'),
        ('OTH', 'Other'),
    ]

    name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=3, choices=ORGANIZATION_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Add the created_by field

    def __str__(self):
        return self.name
