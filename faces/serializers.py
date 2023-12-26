from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import Face

class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])


class FaceQuerySerializer(serializers.Serializer):
    face_tokens = serializers.ListField(child=serializers.CharField(), required=False)
    color = serializers.CharField(required=True)


class ListFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ('id', 'image_file', 'face_tokens')
        read_only_fields = fields


class ComparisonSerializer(serializers.Serializer):
    face_token1 = serializers.CharField()
    face_token2 = serializers.CharField()


class ComparisonConfidenceSerializer(serializers.Serializer):
    confidence = serializers.FloatField()
    