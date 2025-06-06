from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from user.models import Contact

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
        
    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )
        if not user:
            raise ValidationError('Invalid credentials')
        
        data['user'] = user
        return data

class ContactSerializer(serializers.Serializer):
    user2 = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        user1 = self.context["request"].user
        user2 = validated_data["user2"]

        contact = Contact.objects.create(user1=user1, user2=user2)
        contact.full_clean()
        contact.save()
        return contact

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "follower": instance.user1.id,
            "followed": instance.user2.id,
        }
