from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        
        user = get_user_model().objects.create_user(
            validated_data["email"],
            validated_data["password"],
        )
        
        return user


# login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")    

