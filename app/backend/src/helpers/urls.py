from django.urls import path

from helpers.views import CheckRamView, WeatherView

urlpatterns = [
    path('check_ram/', CheckRamView.as_view(), name='check-ram'),
    path('weather/', WeatherView.as_view(), name='weather')
]
