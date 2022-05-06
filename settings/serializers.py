from django.contrib.auth.hashers import check_password

from rest_framework import serializers

from settings.models import GlobalConfig


class GlobalConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlobalConfig
        fields = (
            "lookback_period",
            "lookback_override",
            "active_storm",
            "geocode_users",
        )
