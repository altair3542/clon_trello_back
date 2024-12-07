from rest_framework import serializers
from .models import List

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board', 'position', 'created_at', 'updated_at')
        read_only_fields = ('board',)
