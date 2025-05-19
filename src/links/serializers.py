import random
import string

from rest_framework import serializers

from links.models import Link, LinkHit

BASE62_ALPHABET = string.ascii_letters + string.digits


def generate_base62_code(length=6):
    return "".join(random.choices(BASE62_ALPHABET, k=length))


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        link = Link.objects.create(
            **validated_data,
            link_hash=generate_base62_code(),
        )
        return link

    class Meta:
        model = Link
        fields = ["link_hash", "url"]
        read_only_fields = ["link_hash", "hits", "created_at"]


class LinkHitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LinkHit
        fields = ["creation_date"]
        read_only = ["creation_date"]


class LinkHitDetailedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source="link.url")
    link_hash = serializers.CharField(source="link.link_hash")

    class Meta:
        model = LinkHit
        fields = ["url", "link_hash", "creation_date"]
        read_only = ["url", "link_hash", "creation_date"]
