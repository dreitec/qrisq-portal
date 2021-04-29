from django.urls import path
from .views import StormDataView, WindDataView

urlpatterns = [
    path('storm-data', StormDataView.as_view(), name="storm-data"),
    path('wind-data', WindDataView.as_view(), name="storm-data"),
]