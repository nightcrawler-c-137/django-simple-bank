from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

Customer = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}, trim_whitespace=False
        )
    password_confirm = serializers.CharField(
        write_only=True, style={'input_type': 'password'}, trim_whitespace=False
        )
    class Meta:
        model = Customer
        fields = ('email','password', 'password_confirm')

    def validate_password(self, value):
        request = self.context.get('request')
        if value == request.data['password_confirm']:
            return value
        raise serializers.ValidationError('passwords do not match')

    def create(self, validated_data):
        customer = Customer.objects.create_user(
            email=validated_data['email']
        )

        customer.set_password(validated_data['password'])
        customer.save()
        return customer
        

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email', 'wallet')
