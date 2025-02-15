from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROLE_CHOICES = [
        ('secretary', 'Secretary'),
        ('blood_secretary', 'Blood Secretary'),
        ('member', 'Member'),
    ]

class Role(models.Model):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.role

class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.OneToOneField(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class BloodSecretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    secretary = models.OneToOneField(Secretary, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    secretary = models.ForeignKey(Secretary, on_delete=models.CASCADE)
    blood_secretary = models.ForeignKey(BloodSecretary, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"Member: {self.user.first_name} {self.user.last_name} - {self.role.role}"
