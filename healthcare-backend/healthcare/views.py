from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from .models import User, Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer,
    PatientDoctorMappingCreateSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user).select_related('user')

    def perform_create(self, serializer):
        # Create patient user automatically
        user = User.objects.create(
            username=serializer.validated_data['user']['username'],
            email=serializer.validated_data['user']['email'],
            first_name=serializer.validated_data['user']['first_name'],
            last_name=serializer.validated_data['user']['last_name'],
            is_patient=True
        )
        user.set_password('temporary_password')  # In production, generate a random password
        user.save()
        serializer.save(user=user, created_by=self.request.user)

class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user).select_related('user')

class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(created_by=self.request.user).select_related('user')

    def perform_create(self, serializer):
        # Create doctor user automatically
        user = User.objects.create(
            username=serializer.validated_data['user']['username'],
            email=serializer.validated_data['user']['email'],
            first_name=serializer.validated_data['user']['first_name'],
            last_name=serializer.validated_data['user']['last_name'],
            is_doctor=True
        )
        user.set_password('temporary_password')  # In production, generate a random password
        user.save()
        serializer.save(user=user, created_by=self.request.user)

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(created_by=self.request.user).select_related('user')

class PatientDoctorMappingViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PatientDoctorMappingCreateSerializer
        return PatientDoctorMappingSerializer

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related('patient', 'doctor', 'patient__user', 'doctor__user')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        patient = serializer.validated_data['patient']
        doctor = serializer.validated_data['doctor']
        
        if patient.created_by != request.user:
            return Response(
                {"error": "You can only assign doctors to your own patients"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            return Response(
                {"error": "This doctor is already assigned to this patient"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PatientDoctorMappingsByPatientView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientDoctorMapping.objects.filter(
            patient_id=patient_id,
            patient__created_by=self.request.user
        ).select_related('patient', 'doctor', 'patient__user', 'doctor__user')