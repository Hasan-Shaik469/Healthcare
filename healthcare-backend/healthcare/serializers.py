from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Patient, Doctor, PatientDoctorMapping

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        min_length=8,
        required=True
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'is_patient',
            'is_doctor'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_doctor': user.is_doctor,
            'is_patient': user.is_patient
        })
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_doctor', 'is_patient']
        read_only_fields = ['id', 'is_doctor', 'is_patient']

class PatientSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class DoctorSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ['patient', 'doctor', 'notes']
        extra_kwargs = {
            'patient': {'required': True},
            'doctor': {'required': True}
        }

    def validate(self, data):
        request = self.context.get('request')
        if data['patient'].created_by != request.user:
            raise serializers.ValidationError({
                'patient': 'You can only assign doctors to your own patients'
            })
        return data

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_details = serializers.SerializerMethodField()
    doctor_details = serializers.SerializerMethodField()
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_patient_details(self, obj):
        return {
            'id': obj.patient.user.id,
            'name': f"{obj.patient.user.first_name} {obj.patient.user.last_name}",
            'date_of_birth': obj.patient.date_of_birth,
            'gender': obj.patient.get_gender_display(),
        }

    def get_doctor_details(self, obj):
        return {
            'id': obj.doctor.user.id,
            'name': f"Dr. {obj.doctor.user.first_name} {obj.doctor.user.last_name}",
            'specialization': obj.doctor.get_specialization_display(),
            'hospital': obj.doctor.hospital,
        }

class PatientWithDoctorsSerializer(serializers.ModelSerializer):
    assigned_doctors = serializers.SerializerMethodField()
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def get_assigned_doctors(self, obj):
        mappings = PatientDoctorMapping.objects.filter(patient=obj)
        return PatientDoctorMappingSerializer(mappings, many=True).data

class DoctorWithPatientsSerializer(serializers.ModelSerializer):
    assigned_patients = serializers.SerializerMethodField()
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'

    def get_assigned_patients(self, obj):
        mappings = PatientDoctorMapping.objects.filter(doctor=obj)
        return PatientDoctorMappingSerializer(mappings, many=True).data