from .models import (SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2,
                     Weverse, CrowdtangleInstagram, CrowdtangleFacebook, Vlive, Melon, Spotify)
from rest_framework import serializers


class SocialbladeYoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialbladeYoutube
        fields = "__all__"


class SocialbladeTiktokSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialbladeTiktok
        fields = "__all__"


class SocialbladeTwitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialbladeTwitter
        fields = "__all__"


class SocialbladeTwitter2Serializer(serializers.ModelSerializer):
    class Meta:
        model = SocialbladeTwitter2
        fields = "__all__"


class WeverseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weverse
        fields = "__all__"


class CrowdtangleInstagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrowdtangleInstagram
        fields = "__all__"


class CrowdtangleFacebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrowdtangleFacebook
        fields = "__all__"


class VliveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlive
        fields = "__all__"


class MelonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Melon
        fields = "__all__"


class SpotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Spotify
        fields = "__all__"
