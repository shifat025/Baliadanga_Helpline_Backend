from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Donor

@shared_task
def update_donor_availability():
    """Update is_available for all donors based on their last donation date."""
    four_months_ago = timezone.now().date() - timedelta(days=120)

    # Donors who haven't donated in the last 4 months are marked as available
    Donor.objects.filter(last_donation_date__lte=four_months_ago).update(is_available=True)
    
    # Donors who have donated within the last 4 months are not available
    Donor.objects.filter(last_donation_date__gt=four_months_ago).update(is_available=False)


    # Todo for cellery make setting
