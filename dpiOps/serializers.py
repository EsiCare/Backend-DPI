
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



from .models import Baio_test

class BaioTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baio_test
        fields = "__all__"


class RadioTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radio_test
        fields = "__all__"