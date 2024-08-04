from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import City, Product, Photo
from .services import ProductsService


class ProductListViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.service = ProductsService()

        self.city1 = City.objects.create(name="Paris")
        self.city2 = City.objects.create(name="New York")

        self.product1 = Product.objects.create(name="Donut")
        self.product2 = Product.objects.create(name="Doner")
        self.product3 = Product.objects.create(name="Burger")
        self.product4 = Product.objects.create(name="Macaron")

        self.photo1 = Photo.objects.create(
            product=self.product1, city=self.city1,
            image="photos/ParisDonut.jpg"
        )

        self.photo2 = Photo.objects.create(
            product=self.product3, city=None, image="photos/Burger.jpg"
        )
        self.photo3 = Photo.objects.create(
            product=self.product4, city=None, image="photos/Macaron.jpg"
        )

    def test_get_products_with_city_photos(self):
        """
        Убедитесь, что продукты с фотографиями
        для указанного города возвращаются правильно.
        """
        response = self.client.get(
            reverse("product-list"), HTTP_CITY_ID=str(self.city1.id)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        donut = next(item for item in response.data
                     if item["id"] == self.product1.id)
        self.assertEqual(
            donut["photos"][0]["url"],
            "http://127.0.0.1:8000/media/photos/ParisDonut.jpg")

    def test_get_products_with_global_photos(self):
        """
        Убедитесь, что продукты с глобальными фотографиями возвращаются,
        если фотографии для указанного города отсутствуют.
        """
        response = self.client.get(
            reverse("product-list"), HTTP_CITY_ID=str(self.city2.id)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        burger = next(item for item in response.data
                      if item["id"] == self.product3.id)
        macaron = next(item for item in response.data
                       if item["id"] == self.product4.id)

        self.assertEqual(
            burger["photos"][0]["url"],
            "http://127.0.0.1:8000/media/photos/Burger.jpg")
        self.assertEqual(
            macaron["photos"][0]["url"],
            "http://127.0.0.1:8000/media/photos/Macaron.jpg")

    def test_get_products_without_city_id(self):
        """
        Убедитесь, что при отсутствии заголовка City-ID возвращается ошибка.
        """
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "City-ID header is required")

    def test_get_products_with_invalid_city_id(self):
        """
        Убедитесь, что при передаче неверного City-ID возвращается ошибка.
        """
        response = self.client.get(reverse("product-list"), HTTP_CITY_ID="999")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "City-ID is not correct")

    def test_service_get_products_with_city_photos(self):
        """
        Убедитесь, что сервис возвращает продукты с
        фотографиями для указанного города.
        """
        response = self.service.get_products(city_id=str(self.city1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        donut = next(item for item in response.data
                     if item["id"] == self.product1.id)
        self.assertEqual(
            donut["photos"][0]["url"],
            "http://127.0.0.1:8000/media/photos/ParisDonut.jpg"
        )

    def test_service_get_products_with_global_photos(self):
        """
        Убедитесь, что сервис возвращает продукты с глобальными фотографиями,
        если фотографии для указанного города отсутствуют.
        """
        response = self.service.get_products(city_id=str(self.city2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        burger = next(item for item in response.data
                      if item["id"] == self.product3.id)
        macaron = next(item for item in response.data
                       if item["id"] == self.product4.id)

        self.assertEqual(
            burger["photos"][0]["url"],
            "http://127.0.0.1:8000/media/photos/Burger.jpg"
        )
        self.assertEqual(
            macaron["photos"][0]["url"],
            "http://127.0.0.1:8000/media/photos/Macaron.jpg"
        )
