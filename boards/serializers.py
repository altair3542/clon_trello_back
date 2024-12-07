from rest_framework import serializers
from .models import Board
from django.contrib.auth.models import User

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class BoardSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    members = UserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'name', 'owner', 'members', 'created_at', 'updated_at')

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('name',)
