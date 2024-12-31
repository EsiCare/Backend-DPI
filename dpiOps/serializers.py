
from rest_framework import serializers
from dpiOps.models import *
from .models import Baio_test


class MedCondSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCondition
        fields = "__all__"

class MedCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Care
        fields = "__all__"


class BaioTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baio_test
        fields = "__all__"


class RadioTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radio_test
        fields = "__all__"

class NurseTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse_test
        fields = "__all__"