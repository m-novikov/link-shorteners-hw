from links.models import Link
from rest_framework import serializers
import string, random

BASE62_ALPHABET = string.ascii_letters + string.digits


def generate_base62_code(length=6):
    return ''.join(random.choices(BASE62_ALPHABET, k=length))

class LinkSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        link = Link.objects.create(
             **validated_data,
             link_hash=generate_base62_code(),
        )
        return link
      
    class Meta:
        model = Link
        fields = ['link_hash', 'url']
        read_only_fields = ['link_hash', 'hits', 'created_at']
    