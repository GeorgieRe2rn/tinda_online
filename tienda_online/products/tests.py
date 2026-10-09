from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, Product
from django.urls import reverse


class PrecioFinalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        get_user_model().objects.create_user(
            username='precio-user', password='precio-password'
        )
        electronics = Category.objects.create(name='Electrónica')
        clothing = Category.objects.create(name='Ropa')
        self.laptop = Product.objects.create(
            name='Laptop', category=electronics, price=Decimal('15000.00')
        )
        self.shirt = Product.objects.create(
            name='Camisa', category=clothing, price=Decimal('500.00')
        )
        self.url = reverse('precio-final')

    def test_authenticated_final_price_returns_200(self):
        token_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'precio-user', 'password': 'precio-password'
        }, format='json')
        self.assertEqual(token_response.status_code, 200)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token_response.data['access']
        )
        for product, expected in [
            (self.laptop, '13500.00'), (self.shirt, '400.00')
        ]:
            with self.subTest(category=product.category.name):
                response = self.client.get(self.url, {'product_id': product.pk})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data['final_price'], expected)
                self.assertEqual(response.data['category'], product.category.name)

    def test_final_price_without_token_returns_401(self):
        response = self.client.get(self.url, {'product_id': self.laptop.pk})
        self.assertEqual(response.status_code, 401)


class CategoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            username='test-user',
            password='test-password',
        )
        self.client.force_authenticate(user=user)
        self.category = Category.objects.create(name='Electrónica')

    def test_create_category(self):
        response = self.client.post(
            '/api/categories/',
            {'name': 'Ropa'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Ropa')

    def test_list_categories(self):
        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Electrónica')


class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            username='test-user',
            password='test-password',
        )
        self.client.force_authenticate(user=user)
        self.category = Category.objects.create(name='Electrónica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            price=Decimal('15000.00'),
        )

    def test_create_product(self):
        response = self.client.post(
            '/api/products/',
            {'name': 'Mouse', 'price': '500.00'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name='Mouse').exists())

    def test_list_products_and_filter_by_category(self):
        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category'], 'Electrónica')

        filtered_response = self.client.get(
            '/api/products/',
            {'category': self.category.pk},
        )

        self.assertEqual(filtered_response.status_code, 200)
        self.assertEqual(len(filtered_response.data), 1)
        self.assertEqual(filtered_response.data[0]['name'], 'Laptop')

    def test_update_product(self):
        response = self.client.put(
            f'/api/products/{self.product.pk}/',
            {'name': 'Laptop Pro', 'price': '18000.00'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')
        self.assertEqual(self.product.price, Decimal('18000.00'))

    def test_delete_product(self):
        response = self.client.delete(f'/api/products/{self.product.pk}/')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
