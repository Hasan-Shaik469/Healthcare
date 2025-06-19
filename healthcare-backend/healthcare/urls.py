from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    PatientListCreateView,
    PatientRetrieveUpdateDestroyView,
    DoctorListCreateView,
    DoctorRetrieveUpdateDestroyView,
    PatientDoctorMappingViewSet,
    PatientDoctorMappingsByPatientView
)

router = DefaultRouter()
router.register(r'mappings', PatientDoctorMappingViewSet, basename='mapping')

urlpatterns = [
    # Authentication
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    
    # Patient endpoints
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient-retrieve-update-destroy'),
    
    # Doctor endpoints
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor-retrieve-update-destroy'),
    
    # Mapping endpoints
    path('mappings/patient/<int:patient_id>/', PatientDoctorMappingsByPatientView.as_view(), name='mappings-by-patient'),
    
    # Include router URLs
    path('', include(router.urls)),
]
