from django.urls import path
from .views import (
    SecretaryRegisterView,
    BloodSecretaryRegisterView,
    MemberRegisterView,
    LoginView,
    SecretaryUpdateView,
    BloodSecretaryUpdateView,
    ResetSecretaryPasswordView,
    ResetBloodSecretaryPassword,
    BloodSecretaryListView,
    ResetMemberPassword
)


urlpatterns = [
    path('register/secretary/', SecretaryRegisterView.as_view(), name='register-secretary'),
    path('register/blood-secretary/', BloodSecretaryRegisterView.as_view(), name='register-blood-secretary'),
    path('register/member/', MemberRegisterView.as_view(), name='register-member'),
    path('secretary/update/', SecretaryUpdateView.as_view(), name='secretary-update'),
    path('blood-secretary/update/<int:blood_secretary_id>/', SecretaryUpdateView.as_view(), name='blood-secretary-update'),
    path('secretary/update/member/<int:member_id>/', SecretaryUpdateView.as_view(), name='update-member-secretary'),
    path('blood-secretary/update/member/<int:member_id>/', BloodSecretaryUpdateView.as_view(), name='update-member-blood-secretary'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-secretary-password/', ResetSecretaryPasswordView.as_view(), name='reset-secretary-password'),
    path('blood-secretaries/', BloodSecretaryListView.as_view(), name='blood-secretary-list'),
    path('reset-blood-secretary-password/', ResetBloodSecretaryPassword.as_view(), name='reset_blood_secretary_password'),
    path('reset-member-password/', ResetMemberPassword.as_view(), name='reset-member-password'),
]
