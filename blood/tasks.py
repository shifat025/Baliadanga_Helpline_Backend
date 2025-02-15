from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Donor

@shared_task
def update_donor_availability():
    four_months_ago = timezone.now().date() - timedelta(days=120)
    Donor.objects.filter(last_donation_date__lte=four_months_ago).update(is_available=True)
    Donor.objects.filter(last_donation_date__gt=four_months_ago).update(is_available=False)
