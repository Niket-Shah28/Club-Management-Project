from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class usermodel(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=USER
        fields='__all__'

    def create(self,validated_data):
        user=USER(
            First_Name=validated_data['First_Name'],
            Middle_Name=validated_data['Middle_Name'],
            Last_Name=validated_data['Last_Name'],
            password=validated_data['password'],
            Gender=validated_data['Gender'],
            Salutation=validated_data['Salutation'],
            email=validated_data['email'],
            Contact_no=validated_data['Contact_no'],
            Emergency_contact_no=validated_data['Emergency_contact_no'],
            Date_of_Birth=validated_data['Date_of_Birth'],
            Address_line_1=validated_data['Address_line_1'],
            Address_line_2=validated_data['Address_line_2'],
            State=validated_data['State'],
            City=validated_data['City'],
            Pincode=validated_data['Pincode'],
            Id_Proof_name=validated_data['Id_Proof_name'],
            Id_Proof_no=validated_data['Id_Proof_no'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class manager(serializers.ModelSerializer):
    class Meta:
        model=Manager
        fields='__all__'