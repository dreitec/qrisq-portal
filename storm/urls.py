from django.urls import path
from .views import StormDataView

urlpatterns = [
    path('storm-data', StormDataView.as_view(), name="storm-data"),
]