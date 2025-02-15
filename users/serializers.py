from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, Secretary, BloodSecretary, Member

# Serializer for user registration
class RegisteSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False, default=None)  # Role field (only for input)
    confirm_password = serializers.CharField(required=True)  # Password confirmation field

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password', 'role')

    # Function to check if passwords match and email is unique
    def validate(self, data):
        if data['password'] != data['confirm_password']:  # Check if passwords are the same
            raise serializers.ValidationError({'error': "Password doesn't match"})

        if User.objects.filter(email=data['email']).exists():  # Check if email is already used
            raise serializers.ValidationError({'error': "Email already exists"})

        return data

    # Function to create a user with a role
    def create(self, validated_data):
        # Create the user
        user_data = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email'],
            'username': validated_data['email'].split('@')[0],  # Username from email
        }

        user = User.objects.create(**user_data)  # Create user
        user.set_password(validated_data['password'])  # Hash password
        user.save()

        # Get role instance
        role = validated_data['role']
        role_instance = Role.objects.get(role=role)

        secretary = None
        blood_secretary = None

        if role == 'secretary':
            # Create a secretary if none exists
            secretary, created = Secretary.objects.get_or_create(role=role_instance, user=user)
            if not created:  # If secretary already exists, show an error
                raise serializers.ValidationError({'error': "Secretary already exists"})

        elif role == 'blood_secretary':
            try:
                # Get the secretary (only one should exist)
                secretary = Secretary.objects.get(role=Role.objects.get(role='secretary'))
            except Secretary.DoesNotExist:
                raise serializers.ValidationError({'error': "No Secretary found for this blood secretary"})

            # Check if a blood secretary already exists for the secretary
            if BloodSecretary.objects.filter(secretary=secretary).exists():
                raise serializers.ValidationError({'error': "Cannot add more blood secretaries"})

            # Create a BloodSecretary
            blood_secretary = BloodSecretary.objects.create(
                role=role_instance,
                secretary=secretary,
                user=user  # Assign user
            )

        elif role == 'member':
            try:
                # Get secretary and blood secretary
                secretary = Secretary.objects.get(role=Role.objects.get(role='secretary'))
                blood_secretary = BloodSecretary.objects.get(secretary=secretary)
            except (Secretary.DoesNotExist, BloodSecretary.DoesNotExist):
                raise serializers.ValidationError({'error': "A Secretary or Blood Secretary must be assigned to this member."})

            # Create a member
            member = Member.objects.create(
                user=user,  # Assign user
                secretary=secretary,
                blood_secretary=blood_secretary,
                role=role_instance
            )

        user.save()
        return user  # Return created user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    

class BloodSecretarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodSecretary
        fields = '__all__'