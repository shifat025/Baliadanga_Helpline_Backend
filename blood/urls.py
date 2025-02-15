# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonorCreateView, DonorListView,DonorUpdateView,BloodHistoryAPIView



urlpatterns = [
    path('donors/', DonorListView.as_view(), name='donor-list'),
    path('create-donor/', DonorCreateView.as_view(), name='create-donor'),
    path('donors/<int:pk>/update/', DonorUpdateView.as_view(), name='update_donor'),
    path('blood-donations/<int:donor_id>/', BloodHistoryAPIView.as_view(), name='blood-donation-history'),

]
