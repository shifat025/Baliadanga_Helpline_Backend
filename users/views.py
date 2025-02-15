from django.conf import settings  # Import settings to access your configuration
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisteSerializer, UserUpdateSerializer, BloodSecretarySerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Secretary, BloodSecretary,Member
from users.permission import BloodSecretaryPermission

class SecretaryRegisterView(APIView):
    def post(self, request):
        serializer = RegisteSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BloodSecretaryRegisterView(APIView):
    # permission_classes = [IsAuthenticated,RoleBasedPermission('secretary')]
    def post(self, request):
        serializer = RegisteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blood Secretary registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MemberRegisterView(APIView):
    def post(self, request):
        serializer = RegisteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Member registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BloodSecretaryListView(APIView):
    def get(self, request):
        blood_secretaries = BloodSecretary.objects.all()
        serializer = BloodSecretarySerializer(blood_secretaries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Todo login with email and number
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Get the role associated with the user
        try:
            role = None
            if hasattr(user, 'secretary'):
                role = 'secretary'
            elif hasattr(user, 'bloodsecretary'):
                role = 'blood_secretary'
            elif hasattr(user, 'member'):
                role = 'member'

            return Response({
                'user_id': user.id,
                'token': access_token,
                'role': role
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class SecretaryUpdateView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission('secretary')]

    def patch(self, request):
        try:
            secretary = Secretary.objects.get(user = request.user)
        except Secretary.DoesNotExist:
            return Response({'error': 'Secretary not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserUpdateSerializer(secretary.user, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Secretary updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_blood_secretary(self, request, blood_secretary_id):
        try:
            secretary = Secretary.objects.get(user=request.user)
            blood_secretary = BloodSecretary.objects.get(id = blood_secretary_id, secretary = secretary)
        
        except (Secretary.DoesNotExist, BloodSecretary.DoesNotExist):
            return Response({'error': 'Blood Secretary not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserUpdateSerializer(blood_secretary.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blood Secretary updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_member(self, request, member_id):
        try:
            secretary = Secretary.objects.get(user=request.user)
            member = Member.objects.get(id=member_id, secretary=secretary)
        except (Secretary.DoesNotExist, Member.DoesNotExist):
            return Response({'error': 'Member not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserUpdateSerializer(member.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Member updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BloodSecretaryUpdateView(APIView):
    # permission_classes = [IsAuthenticated, RoleBasedPermission('blood_secretary')]
    
    def update_member(self, request, member_id):
        try:
            blood_secretary = BloodSecretary.objects.get(user=request.user)
            member = Member.objects.get(id=member_id, blood_secretary=blood_secretary)
        except (BloodSecretary.DoesNotExist, Member.DoesNotExist):
            return Response({'error': 'Member not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserUpdateSerializer(member.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Member updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ResetSecretaryPasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        try:
            # Get the authenticated user and their secretary instance
            user = request.user
            secretary = Secretary.objects.get(user=user)
            
            # Generate a password with 2 or 3 letters, 2 or 3 numbers, and 1 or 2 special characters
            letters = random.choices(string.ascii_letters, k=3)  # 2 or 3 letters
            numbers = random.choices(string.digits, k=2)  # 2 numbers
            special_characters = random.choices(['@', '#'], k=2)  # 1 or 2 special characters
            
            # Combine and shuffle the characters to ensure randomness
            password_characters = letters + numbers + special_characters
            random.shuffle(password_characters)
            new_password = ''.join(password_characters)
            
            # Set and save the new password for the user
            user.set_password(new_password)
            user.save()
            
            # Prepare email content using the template
            email_body = render_to_string(
                'secretary_password_reset.html', 
                {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'new_password': new_password
                }
            )
            
            # Send the new password to the secretary's email
            send_mail(
                subject="Password Reset for Your Account",
                message=email_body,  # This will send the HTML content
                from_email=settings.EMAIL_HOST_USER,  # Get the email from settings
                recipient_list=[user.email],
                fail_silently=False,
                html_message=email_body  # Include the HTML message in the email
            )
            
            return Response({"message": "Password reset successfully. Check your email."}, status=status.HTTP_200_OK)
        
        except Secretary.DoesNotExist:
            return Response({"error": "Authenticated user is not a secretary."}, status=status.HTTP_400_BAD_REQUEST)


class ResetBloodSecretaryPassword(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        try:
            # Get the authenticated user
            user = request.user
            secretary = Secretary.objects.get(user=user)
           
            
            # Get the blood secretary to reset password for
            blood_secretary_id = request.data.get('blood_secretary_id')
            if not blood_secretary_id:
                return Response({"error": "Blood Secretary ID is required."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                blood_secretary = BloodSecretary.objects.get(id=blood_secretary_id)
            except BloodSecretary.DoesNotExist:
                return Response({"error": "Blood Secretary not found."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Generate a password with 2 or 3 letters, 2 or 3 numbers, and 1 or 2 special characters
            letters = random.choices(string.ascii_letters, k=3)  # 2 or 3 letters
            numbers = random.choices(string.digits, k=2)  # 2 numbers
            special_characters = random.choices(['@', '#'], k=2)  # 1 or 2 special characters
            
            # Combine and shuffle the characters to ensure randomness
            password_characters = letters + numbers + special_characters
            random.shuffle(password_characters)
            new_password = ''.join(password_characters)
            
            # Set and save the new password for the blood secretary
            blood_secretary.user.set_password(new_password)
            blood_secretary.user.save()
            
            # Prepare email content for the blood secretary
            email_body = render_to_string(
                'blood_secretary_password_reset.html', 
                {
                    'first_name': blood_secretary.user.first_name,
                    'last_name': blood_secretary.user.last_name,
                    'new_password': new_password
                }
            )
            
            # Send the new password to the blood secretary's email
            send_mail(
                subject="Password Reset for Your Account",
                message=email_body,  # This will send the HTML content
                from_email=settings.EMAIL_HOST_USER,  # Get the email from settings
                recipient_list=[blood_secretary.user.email],
                fail_silently=False,
                html_message=email_body  # Include the HTML message in the email
            )
            
            # Prepare email content to notify the secretary about the password reset
            secretary_email_body = render_to_string(
                'blood_secretary_password_reset_notification.html', 
                {
                    'first_name': blood_secretary.user.first_name,
                    'last_name': blood_secretary.user.last_name,
                    'new_password': new_password
                }
            )
            # Send an email to the secretary informing them of the blood secretary's password reset
            send_mail(
                subject="Blood Secretary Password Reset",
                message=secretary_email_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[secretary.user.email],  # Send to the secretary's email
                fail_silently=False,
                html_message=secretary_email_body
            )
            
            return Response({"message": "Blood secretary password reset successfully. Check the email."}, 
                            status=status.HTTP_200_OK)
        
        except Secretary.DoesNotExist:
            return Response({"error": "Authenticated user is not a secretary."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        

class ResetMemberPassword(APIView):
    permission_classes = [IsAuthenticated, BloodSecretaryPermission]  # Ensure the user is authenticated

    def post(self, request):
        try:
            # Get the authenticated user
            user = request.user
            blood_secretary = BloodSecretary.objects.get(user=user)


            # Get the Member to reset password for
            member_id = request.data.get('member_id')
            if not member_id:
                return Response({"error": "Member ID is required."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                member = Member.objects.get(id=member_id, blood_secretary=blood_secretary)
            except Member.DoesNotExist:
                return Response({"error": "Member not found or not under this blood secretary."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Generate a new password
            letters = random.choices(string.ascii_letters, k=3)
            numbers = random.choices(string.digits, k=2)
            special_characters = random.choices(['@', '#'], k=2)
            password_characters = letters + numbers + special_characters
            random.shuffle(password_characters)
            new_password = ''.join(password_characters)

            # Set and save the new password for the member
            member.user.set_password(new_password)
            member.user.save()

            # Prepare email content for the member
            email_body = render_to_string(
                'member_password_reset.html',
                {
                    'first_name': member.user.first_name,
                    'last_name': member.user.last_name,
                    'new_password': new_password
                }
            )

            # Send the new password to the member's email
            send_mail(
                subject="Password Reset for Your Account",
                message=email_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[member.user.email],
                fail_silently=False,
                html_message=email_body
            )

            # Notify the Blood Secretary
            blood_secretary_email_body = render_to_string(
                'blood_secretary_member_password_reset_notification.html',
                {
                    'member_first_name': member.user.first_name,
                    'member_last_name': member.user.last_name,
                    'new_password': new_password
                }
            )

            send_mail(
                subject="Member Password Reset Notification",
                message=blood_secretary_email_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[blood_secretary.user.email],
                fail_silently=False,
                html_message=blood_secretary_email_body
            )

            return Response({"message": "Member password reset successfully. Check the email."}, 
                            status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

