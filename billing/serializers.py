from django.contrib.auth.hashers import check_password

from rest_framework import serializers

from billing.models import Billing


class BillingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Billing
        fields = (
            "id",
            "type",
            "city",
            "county",
            "state",
            "status",
            "start_date",
            "end_date",
            "discount",
            "users",
            "shape_file"
        )
