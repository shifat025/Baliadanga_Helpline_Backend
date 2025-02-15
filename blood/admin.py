from django.contrib import admin
from .models import Donor, BloodHistory, BloodRequest

class DonorAdmin(admin.ModelAdmin):
    list_display = ( 'blood_type', 'contact_number', 'location', 'last_donation_date', 'total_blood_donated', 'is_available')
    search_fields = ('user__username', 'contact_number', 'location')
    list_filter = ('blood_type', 'is_available')
    ordering = ('-last_donation_date',)

class BloodHistoryAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_date', 'blood_donated')
    search_fields = ('donor__user__username', 'donation_date')
    list_filter = ('donation_date',)
    ordering = ('-donation_date',)

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('blood_type', 'location', 'requested_by', 'is_fulfilled', 'created_at')
    search_fields = ('blood_type', 'location', 'requested_by__username')
    list_filter = ('blood_type', 'is_fulfilled')
    ordering = ('-created_at',)

# Register the models with the admin site
admin.site.register(Donor, DonorAdmin)
admin.site.register(BloodHistory, BloodHistoryAdmin)
admin.site.register(BloodRequest, BloodRequestAdmin)
