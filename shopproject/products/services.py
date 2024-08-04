from rest_framework.response import Response
from rest_framework import status

from .models import Product, Photo, City


class ProductsService:
    def __init__(self):
        pass

    def _format_photos(self, photos, product):
        """
        Форматирует данные о продукте,
        добавляя полные URL-адреса для фотографий продукта.

        Аргументы:
        photos (QuerySet): Набор фотографий, связанных с продуктом.
        product (Product): Объект продукта,
        для которого нужно отформатировать данные.

        Возвращает:
        dict: Словарь с отформатированными данными о продукте,
        включающий id, имя и URL-адреса фотографий.
        """
        photos_data = [
            {"url": f"http://127.0.0.1:8000/media/{photo.image}"}
            for photo in photos
        ]

        return {
            "id": product.id,
            "name": product.name,
            "photos": photos_data,
        }

    def get_products(self, city_id: str) -> Response:
        """
        Получает список продуктов с фотографиями,
        отфильтрованными по указанному ID города.

        Аргументы:
        city_id (str): ID города, для которого нужно получить фотографии.

        Возвращает:
        Response: Объект ответа с отформатированными
        данными о продуктах и фотографиях.
        """
        cities = City.objects.all()
        cities_ids = [city.pk for city in cities]
        if int(city_id) not in cities_ids:
            return Response(
                {"detail": "City-ID is not correct"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        products = Product.objects.all()
        result = []

        if not Photo.objects.filter(city_id=city_id).exists():
            for product in products:
                photos = Photo.objects.filter(product=product,
                                              city__isnull=True)
                result.append(self._format_photos(photos=photos,
                                                  product=product))

        else:
            for product in products:
                photos = Photo.objects.filter(product=product,
                                              city_id=city_id)
                result.append(self._format_photos(photos=photos,
                                                  product=product))

        return Response(result, status=status.HTTP_200_OK)
