from rest_framework import serializers
from .models import Category, Area, News, Comment, User, District
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']

class AreaSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    district_id = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), source='district', write_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'district', 'district_id']

class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    area_id = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all(), source='area', write_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'category', 'area', 'category_id', 'area_id', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'news', 'user', 'content', 'created_at']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        return user
