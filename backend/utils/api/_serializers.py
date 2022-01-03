from rest_framework import serializers


class UsernameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    real_name = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.need_real_name = kwargs.pop("need_real_name", False)
        super().__init__(*args, **kwargs)
