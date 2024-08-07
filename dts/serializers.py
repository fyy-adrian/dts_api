from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .serializers import *
from .models import *
from django.urls import reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Tambahkan klaim grup pengguna
        groups = user.groups.values_list('name', flat=True)
        token['groups'] = list(groups)

        return token
    
class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        # Tambahkan klaim grup pengguna
        groups = user.groups.values_list('name', flat=True)
        token['groups'] = list(groups)

        return token

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserDetailSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email' , 'groups',]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'groups')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'groups')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Validasi tambahan jika diperlukan
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        groups = validated_data.pop('groups', None)

        user = User.objects.create(**validated_data)
        user.set_password(password)

        if groups is not None:
            user.groups.set(groups)

        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    old_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'old_password', 'groups')
        extra_kwargs = {
            'password': {'write_only': True},
            'old_password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        old_password = data.get('old_password')

        if password and not old_password:
            raise serializers.ValidationError({"old_password": "Old password is required when updating password."})

        if old_password and not password:
            raise serializers.ValidationError({"password": "New password is required when old password is provided."})

        return data

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password', None)
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)

        if password:
            if not old_password:
                raise serializers.ValidationError({"old_password": "Old password is required when updating password."})
            if not instance.check_password(old_password):
                raise serializers.ValidationError({"old_password": "Old password is incorrect."})
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if groups is not None:
            instance.groups.set(groups)

        instance.save()
        return instance

class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PortofolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portofolio
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = '__all__'

class CombinedSerializer(serializers.Serializer):
    hero = HeroSerializer(allow_null=True)  # Mengizinkan nilai null jika tidak ada hero yang aktif
    prices = PriceSerializer(many=True)
    services = ServiceSerializer(many=True)
    portofolios = PortofolioSerializer(many=True)
    partnerships = PartnershipSerializer(many=True)

def add_absolute_url(data, request, fields):
    if isinstance(data, dict):
        for field in fields:
            if field in data and data[field]:
                data[field] = request.build_absolute_uri(data[field])
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                add_absolute_url(item, request, fields)
