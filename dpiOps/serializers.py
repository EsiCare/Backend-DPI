
from rest_framework import serializers
from dpiOps.models import *


class MedCondSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCondition
        fields = "__all__"

class MedCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Care
        fields = "__all__"

class PresEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionEntry
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):

    entries = PresEntrySerializer(many = True)

    class Meta:
        model = Prescription
        fields = "__all__"
