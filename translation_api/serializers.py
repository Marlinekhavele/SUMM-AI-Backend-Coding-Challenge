from rest_framework import serializers
from .models import Translation

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'user', 'original_text', 'translated_text', 'content_type', 'created_at', 'target_language']
        read_only_fields = ['id', 'created_at']

