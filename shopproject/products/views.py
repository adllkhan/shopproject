from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http.request import HttpRequest

from .services import ProductsService


services = ProductsService()


class ProductListView(APIView):
    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        city_id = request.headers.get("City-ID")

        if not city_id:
            return Response(
                {"detail": "City-ID header is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        res = services.get_products(city_id=city_id)
        return res
