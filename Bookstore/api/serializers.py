from django.forms import fields
from django.core.validators import RegexValidator
from rest_framework import serializers

from cuser.models import User

class User_create_serializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(regex=r'^\+\d{1,4}?\d{8,11}$', message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed.")
    phone_no = serializers.ModelField(model_field=User()._meta.get_field('phone'), required=True, validators=[phone_regex,])

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_no', 'password']

    def create(self, validated_data):
        fname = validated_data.get('full_name')
        email = validated_data.get('email')
        phone = validated_data.get('phone_no')
        password = validated_data.get('password')
        user = User.objects.create_user(email, password, fname)
        print('Mobile number from User_create_serializer: ', phone)
        user.phone = phone
        return user


class User_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone', 'date_of_birth', 'gender', 'img']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class User_password_reset_serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email',]

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Thers is no user exists with this email id.')
        return value


class User_password_reset_handle_serializer(serializers.Serializer):
    password1 = serializers.CharField(required=True, label='Password', style={'input_type':'password'})
    password2 = serializers.CharField(required=True, label='Confirm Password', style={'input_type':'password'})
    
    class Meta:
        fields = ['password1', 'password2']

    def validate(self, attrs):
        password = attrs.get('password1', None)
        confirm_password = attrs.get('password2', None)

        if not password == confirm_password:
            raise serializers.ValidationError('Password mismatch. Two passwords didn\'t match.')

        return attrs


class User_password_change_serializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, label='Old Password', style={'input_type':'password'})
    new_password = serializers.CharField(required=True, label='New Password', style={'input_type':'password'})
    confirm_password = serializers.CharField(required=True, label='Confirm Password', style={'input_type':'password'})

    class Meta:
        fields = ['old_password', 'new_password', 'confirm_password']

    def validate(self, attrs):
        password1 = attrs.get('new_password')
        password2 = attrs.get('confirm_password')

        if not password1 == password2:
            raise serializers.ValidationError('Password mismatch. Two passwords didn\'t match.')

        return attrs
