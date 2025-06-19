from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('CARDIOLOGY', 'Cardiology'),
        ('DERMATOLOGY', 'Dermatology'),
        ('NEUROLOGY', 'Neurology'),
        ('PEDIATRICS', 'Pediatrics'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('GENERAL', 'General Physician'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    hospital = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_doctors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    date_assigned = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('patient', 'doctor')
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'

    def __str__(self):
        return f"{self.patient} assigned to {self.doctor}"