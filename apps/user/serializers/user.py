from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from apps.projects.serializers import ProjectSerializer
import re
from django.contrib.auth.password_validation import validate_password


class UserListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'position',
                  'email', 'phone', 'project']
        read_only_fields = ['id']

class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'position',
                  'email', 'password', 're_password']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]*$', value):
            raise serializers.ValidationError('Username do not match pattern: r"^[a-zA-Z0-9_]*$"')
        return value

    def validate_first_name(self, value):
        if not re.match(r'^[a-zA-Z]*$', value):
            raise serializers.ValidationError('First name do not match pattern: r"^[a-zA-Z]*$"')
        return value

    def validate_last_name(self, value):
        if not re.match(r'^[a-zA-Z]*$', value):
            raise serializers.ValidationError('Last name do not match pattern: r"^[a-zA-Z]*$"')
        return value

    def validate_password(self, value):
        validate_password(value)
        if value != self.initial_data.get('re_password'):
            raise ValidationError('Passwords do not match!!')
        return value

    def create(self, validated_data):
        validated_data.pop('re_password')
        user = get_user_model()(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

