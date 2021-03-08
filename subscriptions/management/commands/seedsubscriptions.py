from django.core.management.base import BaseCommand, CommandError
from subscriptions.models import SubscriptionPlan
from django.db import IntegrityError

PLANS = [
    {
        "name": "Monthly",
        "price": 5.0
    },
    {
        "name": "Seasonal",
        "price": 25.0
    }
]


class Command(BaseCommand):
    help = 'Seed Subscription Plans'

    def handle(self, *args, **kwargs):
        objs = [SubscriptionPlan(**plan) for plan in PLANS]
        try:
            SubscriptionPlan.objects.bulk_create(objs)
            self.stdout.write("Seed Subscription Plans.")
        except IntegrityError:
            self.stdout.write("Subscription plans already exists.")