from urllib import response
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from sellHouse.models import User, Apartment

# Create your tests here.


class UserTest(APITestCase):
    def setUp(self):
        # Create user and get token for authorization
        url = ('/auth/users/')
        data = {'username': 'kevfortest', 'password': 'zxzxzxAa123',
                're_password': 'zxzxzxAa123', 'email': 'kevfortest@gmail.com'}
        self.client.post(url, data, format='json')
        response = self.client.post(
            '/auth/token/login/', data={'email': 'kevfortest@gmail.com', 'password': 'zxzxzxAa123'}, format='json')
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='token '+token)
        self.user = User.objects.get()


    def test_access_to_the_user_with_unauthorization(self):
        self.client.credentials()
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_detail(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_owner(self):
        data = {'email': 'new_email@example.com', 'username': 'new_username'}
        response = self.client.put(reverse('user-detail', kwargs={'pk': self.user.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_unowner(self):
        newUser = User.objects.create(
            username='test', email='test@example.com', password='test@example.com')
        data = {'email': 'update_email@example.com', 'username': 'update_username'}
        response = self.client.put(
            reverse('user-detail', kwargs={'pk': newUser.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleted_user(self):
        """
            Delete the user owner
        """
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    
class ApartmentTest(APITestCase):
    def setUp(self):
        # Create user and get token for authorization
        url = ('/auth/users/')
        data = {'username': 'kevfortest', 'password': 'zxzxzxAa123',
                're_password': 'zxzxzxAa123', 'email': 'kevfortest@gmail.com'}
        self.client.post(url, data, format='json')
        response = self.client.post(
            '/auth/token/login/', data={'email': 'kevfortest@gmail.com', 'password': 'zxzxzxAa123'}, format='json')
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='token '+token)
        self.user = User.objects.get()

        # Create apartment
        self.apartment = Apartment.objects.create(
            seller=self.user, address='12 test street', district='Thanh Khê', arena=150, price=20000000, description= 'aaaaaaaaa'
        )


    def test_list_apartment(self):
        self.client.credentials()
        response = self.client.get(reverse('apartment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_apartment_detail(self):
        self.client.credentials()
        response = self.client.get(reverse('apartment-detail',kwargs={'pk':self.apartment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_apartment_with_unauthorization(self):
        self.client.credentials()
        response = self.client.post(reverse('apartment-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_apartment_with_authorization(self):
        data = {'address':'50 test street', 'district':'Thanh Khê', 'arena':250, 'price':20000000, 'description':'aaaaaaaaa'}
        response = self.client.post(reverse('apartment-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_apartment_owner(self):
        data = {'address': 'new_address', 'district': 'Thanh Khê',
                'arena': 250, 'price': 20000000, 'description': 'aaaaaaaaa'}
        response = self.client.put(reverse('apartment-detail', kwargs={'pk':self.apartment.id}), data=data, fomart='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_apartment_unowner(self):
        newUser = User.objects.create(username='test', email='test@example.com', password='zxzxzxAa123')
        newAparment = Apartment.objects.create(
            seller=newUser, address='newaddress', district='Thanh Khê', arena=150, price=20000000, description='aaaaaaaaa'
        )
        data = {'address': 'new_address', 'district': 'Thanh Khê',
                'arena': 250, 'price': 20000000, 'description': 'aaaaaaaaa'}
        response = self.client.put(
            reverse('apartment-detail', kwargs={'pk': newAparment.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_apartment(self):
        self.client.delete(reverse('apartment-detail', kwargs={'pk':self.apartment.id}), format='json')


