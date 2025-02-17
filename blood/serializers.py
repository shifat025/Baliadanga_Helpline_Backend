from rest_framework import serializers
from .models import Donor, BloodRequest,BloodHistory
from datetime import date

class DonarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'

    def create(self, validated_data):
        # Remove the is_available field from validated data
        validated_data.pop('is_available', None)

        # Create the Donor instance
        donor = Donor.objects.create(**validated_data)

        # Automatically set is_available based on the last_donation_date
        donor.update_availability()
        
        # Save the donor instance
        donor.save()

        return donor


class DonorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['last_donation_date', 'total_blood_donated']

    def update(self, instance, validated_data):
        # Get the old values to track changes
        old_total_blood_donated = instance.total_blood_donated
        old_last_donation_date = instance.last_donation_date

        # Update the donor information
        instance.last_donation_date = validated_data.get('last_donation_date', instance.last_donation_date)
        instance.total_blood_donated = validated_data.get('total_blood_donated', instance.total_blood_donated)

        # Save the updated donor information
        instance.save()

        # Check if there is a change in total_blood_donated or last_donation_date
        if ('total_blood_donated' in validated_data and instance.total_blood_donated != old_total_blood_donated) or \
           ('last_donation_date' in validated_data and instance.last_donation_date != old_last_donation_date):
            
            # Check if the month has changed in last_donation_date
            if instance.last_donation_date and old_last_donation_date:
                # If the month changed, log the new blood donation in the BloodHistory model
                if instance.last_donation_date.month != old_last_donation_date.month:
                    blood_donated = instance.total_blood_donated - old_total_blood_donated  # Calculate the donation amount

                    # Only create a history record if blood_donated is positive
                    if blood_donated > 0:
                        BloodHistory.objects.create(
                            donor=instance, 
                            blood_donated=blood_donated
                        )

        return instance

   


class BloodDonationHistory(serializers.ModelSerializer):
    class Meta:
        model = BloodHistory
        fields= '__all__'

class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = '__all__'
