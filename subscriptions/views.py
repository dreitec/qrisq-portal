from django.shortcuts import render
from .models import Subscription, UsersSubscription
from .serializers import SubscriptionSerializer, UsersSubscriptionSerializer
from rest_framework import viewsets


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class UsersSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSubscriptionSerializer
    queryset = UsersSubscription.objects.all()