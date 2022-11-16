from datetime import datetime, timedelta

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.utils.check_ram import RamStatisticsDaemon
from helpers.utils.weather import open_weather_api


class CheckRamView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Отдает информацию по RAM памяти
        """
        daemon = RamStatisticsDaemon()
        daemon.start()
        daemon.join()
        return Response(daemon.get_result())


class WeatherView(APIView):
    location_param = openapi.Parameter('location',
                                       openapi.IN_QUERY,
                                       description="Город и код страны, разделенные запятой.",
                                       type=openapi.TYPE_STRING)

    date_param = openapi.Parameter('date',
                                   openapi.IN_QUERY,
                                   description="Дата (за которую нужна погода) гггг-мм-дд.\n"
                                               "По умолчанию вставляется дата запроса",
                                   type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[location_param, date_param])
    def get(self, request, *args, **kwargs):
        """
        Отдает информацию по пагоде в определенном регионе
        """
        # Если не указанна дата, используется сегодняшняя
        if request.query_params.get('date'):
            need_date = datetime.strptime(request.query_params.get('date'), '%Y-%m-%d')
        else:
            need_date = datetime.utcnow()
        result = open_weather_api.get_full_weather_by_date(
            location=request.query_params.get('location', ''),
            date_start=need_date,
            date_end=need_date+timedelta(days=1),
        )
        return Response(result)
