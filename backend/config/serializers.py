from .models import *
from rest_framework import serializers
from dataprocess.serializers import CollectTargetSerializer, PlatformSerializer


class PlatformTargetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformTargetItem
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['platform'] = PlatformSerializer(read_only=True)
        return super(PlatformSerializer, self).to_representation(instance)


class CollectTargetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectTargetItem
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['collect_target'] = CollectTargetSerializer(read_only=True)
        return super(CollectTargetItemSerializer, self).to_representation(instance)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['collect_target'] = CollectTargetSerializer(read_only=True)
        return super(ScheduleSerializer, self).to_representation(instance)


class AuthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthInfo
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['collect_target'] = CollectTargetSerializer(read_only=True)
        return super(AuthInfoSerializer, self).to_representation(instance)
