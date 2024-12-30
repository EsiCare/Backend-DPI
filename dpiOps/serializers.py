
from rest_framework import serializers
from dpiOps.models import *
from dpi.models import *
from dpi.serializers import *


class MedCondSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    class Meta:
        model = MedicalCondition
        fields = "__all__"

class MedCareSerializer(serializers.ModelSerializer):
    nurse = NurseSerializer()
    patient = PatientSerializer()
    medicalCondition = MedCondSerializer()
    class Meta:
        model = Care
        fields = "__all__"

class PresEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionEntry
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):

    entries = PresEntrySerializer(many = True)
    doctor = DoctorSerializer()
    patient = PatientSerializer()
    class Meta:
        model = Prescription
        fields = "__all__"
