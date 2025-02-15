from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

class Donor(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ]
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    contact_number = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=100)
    last_donation_date = models.DateField(null=True, blank=True)
    total_blood_donated = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField()

    def __str__(self):
        return f"{self.contact_number} ({self.blood_type})"
    
    
class BloodHistory(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_history')
    donation_date = models.DateField(auto_now_add=True)
    blood_donated = models.FloatField()  # Store in liters (L)

    def __str__(self):
        return f"{self.donor.user.username} donated {self.blood_donated}L on {self.donation_date}"

class BloodRequest(models.Model):
    blood_type = models.CharField(max_length=3, choices=Donor.BLOOD_TYPES)
    location = models.CharField(max_length=100)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.blood_type} in {self.location}"



    # def update_availability(self):
    #     if self.last_donation_date:
    #         # Check if last donation was within the last 4 months
    #         if timezone.now().date() - self.last_donation_date <= timedelta(days=120):
    #             self.is_available = False
    #         else:
    #             self.is_available = True
    #     else:
    #         self.is_available = True

    # def save(self, *args, **kwargs):
    #     self.update_availability()
    #     super(Donor, self).save(*args, **kwargs)