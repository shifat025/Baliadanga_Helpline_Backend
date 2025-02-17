# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Donor, BloodHistory
from .serializers import DonarSerializer, DonorUpdateSerializer, BloodDonationHistory
from rest_framework.permissions import IsAuthenticated
from users.permission import BloodSecretaryPermission

class DonorCreateView(APIView):
    permission_classes = [IsAuthenticated, BloodSecretaryPermission ]

    def post(self, request):
        serializer = DonarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DonorUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        try:
            donor = Donor.objects.get(pk=pk)
        except Donor.DoesNotExist:
            return Response({'detail': 'Donor not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DonorUpdateSerializer(donor, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonorListView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        donors = Donor.objects.all()
        serializer = DonarSerializer(donors, many=True)
        return Response(serializer.data)



class BloodHistoryAPIView(APIView):
    def get(self, request, donor_id, *args, **kwargs):
        try:
            # Try to retrieve the specific donor object
            donor = Donor.objects.get(id=donor_id)
            
            # If donor exists, filter blood history by donor
            blood_history = BloodHistory.objects.filter(donor=donor)
            
            # Serialize the blood donation history
            serializer = BloodDonationHistory(blood_history, many=True)
            
            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Donor.DoesNotExist:
            # Return a 404 error if the donor doesn't exist
            return Response({"detail": "Donor not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Catch any other unexpected exceptions
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)