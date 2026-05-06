from rest_framework import serializers
from .models import StudentDetails , Signup

class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetails
        fields = '__all__'

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}