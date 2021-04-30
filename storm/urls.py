from django.urls import path
from .views import StormDataView, WindDataView, SurgeDataView

urlpatterns = [
    path('storm-data', StormDataView.as_view(), name="storm-data"),
    path('surge-data', SurgeDataView.as_view(), name="surge-data"),
    path('wind-data', WindDataView.as_view(), name="wind-data"),
]