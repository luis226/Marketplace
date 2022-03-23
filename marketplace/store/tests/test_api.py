from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import User
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
            'stock': '10',
            'name': 'Computer',
            'description': 'An awesome computer',
        }
        
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, 201)
        
        del data['password']
        data['username']  = 'NameLastName'
        self.assertDictEqual(response.json(), data)

    