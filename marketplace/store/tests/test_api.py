from django.urls import reverse
from datetime import datetime
from rest_framework.test import APITestCase
from store.models import User, Product
from freezegun import freeze_time

''' 
TODO: Might be a good idea to separte this into many test classes once the number of tests grow
'''
class UserAPITests(APITestCase):
    def test_get_token(self):
        """
        Ensure the user can get an auth token
        """
        url = reverse('obtain-token')

        user = User.objects.create(
            username='testuser',
            email='test@test.com'
        )

        user.set_password('test')
        user.save()
        data = {
            'username': 'testuser',
            'password': 'test'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertIsNotNone(result.get('token', None))

    def test_can_create_user(self):
        '''
        Check the user creation (register) works        
        '''
        
        # Just to enforce the user is not logged in
        self.client.logout()

        url = reverse('users')

        data = {
            'first_name': 'Name',
            'last_name': 'LastName',
            'email': 'test@test.com',
            'sex': 'male',
            'type': 'buyer',
            'password' : 'Test1234'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        
        del data['password']
        data['username']  = 'NameLastName'
        self.assertDictEqual(response.json(), data)


class ProductsAPITest(APITestCase):
    def setUp(self):
        self.buyer_user = User.objects.create(
            username='buyer',
            type='buyer',
            email='buyer@test.com',
        )
        self.seller_user = User.objects.create(
            username='seller',
            type='seller',
            email='seller@test.com'
        )
        self.url_list = reverse('products-list')
    
    def test_seller_user_can_create_products(self):
        '''
        Check the user creation (register) works        
        '''
        # Only seller user can register a product
        self.client.force_login(self.seller_user)

        data = {
            'price': '120.50',
            'selled_by': str(self.seller_user.uuid),
            'stock': 10,
            'name': 'Computer',
            'description': 'An awesome computer',
        }

        with freeze_time('2020-01-01'):
            response = self.client.post(self.url_list, data)
            self.assertEqual(response.status_code, 201)

        data['created'] = '2020-01-01T00:00:00Z'
        result = response.json()
        del result['uuid']
        self.assertDictEqual(result, data)

    def test_buyer_user_cannot_create_products(self):
        '''
        Check the user creation (register) works
        '''
        # Only seller user can register a product
        self.client.force_login(self.buyer_user)

        data = {
            'price': '120.50',
            'selled_by': str(self.seller_user.uuid),
            'stock': 10,
            'name': 'Computer',
            'description': 'An awesome computer',
        }

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, 403)

    def test_seller_user_only_see_his_products(self):
        other_user = User.objects.create(username='other')
        products = []
        for i in range(5):
            Product.objects.create(
                selled_by=other_user,
                price=10,
                name=f'Product {i}',
                stock=10
            )

            product = Product.objects.create(
                selled_by=self.seller_user,
                price=10,
                name=f'Product {i}',
                stock=10
            )
            products.append(product)
        # Only seller user can register a product
        self.client.force_login(self.seller_user)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

        result = [r['uuid'] for r in response.json()]
        products_uuid = [str(p.uuid) for p in products]

        self.assertCountEqual(result, products_uuid)

    def test_buyer_user_only_see_all_active_products(self):
        other_user = User.objects.create(username='other')
        products = []
        for i in range(5):
            Product.objects.create(
                selled_by=other_user,
                price=10,
                name=f'Product {i}',
                stock=10,
                is_active=False
            )

            product = Product.objects.create(
                selled_by=other_user,
                price=10,
                name=f'Product {i}',
                stock=10
            )
            products.append(product)
        # Only seller user can register a product
        self.client.force_login(self.buyer_user)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

        result = [r['uuid'] for r in response.json()]
        products_uuid = [str(p.uuid) for p in products]

        self.assertCountEqual(result, products_uuid)


class OrderAPITest(APITestCase):
    def setUp(self):
        self.buyer_user = User.objects.create(
            username='buyer',
            type='buyer',
            email='buyer@test.com',
        )
        self.seller_user = User.objects.create(
            username='seller',
            type='seller',
            email='seller@test.com'
        )

        self.product = Product.objects.create(
            selled_by=self.seller_user,
            price=10,
            name=f'Product Test',
            stock=10,
        )

        self.url_list = reverse('orders')

    def test_buyer_can_create_order(self):
        data = {
            'product': str(self.product.uuid),
            'units': 10,
            'buyer': str(self.buyer_user.uuid),
        }

        self.client.force_login(self.buyer_user)

        with freeze_time('2020, 2, 1'):
            response = self.client.post(self.url_list, data)

            self.assertEqual(response.status_code, 201)

        data['status'] = 'cart'
        data['modified'] = None
        data['created'] = '2020-02-01T00:00:00Z'
        self.assertDictEqual(response.json(), data)

    def test_seller_cannot_create_order(self):
        data = {
            'product': str(self.product.uuid),
            'units': 10,
            'buyer': str(self.buyer_user.uuid),
        }

        self.client.force_login(self.seller_user)

        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, 403)


