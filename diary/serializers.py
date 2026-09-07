from rest_framework import serializers
from .models import DiaryEntry

class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = [
            "id",
            "user",
            "title",
            "content",
            "visibility",
            "created_at",
            "updated_at",
        ]
        
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]
    def validate_title(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )

        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must contain at least 3 characters."
            )

        return value

    def validate_content(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Diary content cannot be empty."
            )

        if len(value) < 10:
            raise serializers.ValidationError(
                "Diary content must contain at least 10 characters."
            )

        return value