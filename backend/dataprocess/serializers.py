from .models import Platform, ArtistProfile, Artist, CollectData, CollectTarget
from rest_framework import serializers


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = "__all__"


class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProfile
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class CollectDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectData
        fields = "__all__"

    def to_representation(self, instance):
        self.fields["collect_target"] = CollectTargetSerializer(read_only=True)
        return super(CollectDataSerializer, self).to_representation(instance)


class CollectTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectTarget
        fields = "__all__"

    def to_representation(self, instance):
        self.fields["artist"] = ArtistSerializer(read_only=True, null=True)
        self.fields["platform"] = PlatformSerializer(read_only=True)
        return super(CollectTargetSerializer, self).to_representation(instance)
