from rest_framework import serializers
from .models import User, Trainer, Customer,Train, Schedule


class TrainerRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Trainer
        fields = ('username', 'password', 'password2', 'email', 'age', 'bio', 'experience')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username cant be `admin`')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must match')
        return data


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = (
            'username', 'password', 'password2', 'email', 'age', 'bio', 'historyOfBloodPressure', 'historyOfDiabetes',
            'height', 'weight', 'days')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username cant be `admin`')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must match')
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'type')


class TrainerEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ('email', 'age', 'bio', 'experience')


class CustomerEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email', 'age', 'bio', 'historyOfBloodPressure', 'historyOfDiabetes', 'height', 'weight', 'days')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('train', 'day', 'number')


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ('category', 'name')
