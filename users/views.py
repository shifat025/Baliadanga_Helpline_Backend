from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisteSerializer, UserUpdateSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Secretary, BloodSecretary,Member
# from .permission import RoleBasedPermission

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