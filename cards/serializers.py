from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'title', 'description', 'list', 'position', 'created_at', 'updated_at')
        read_only_fields = ('list',)
