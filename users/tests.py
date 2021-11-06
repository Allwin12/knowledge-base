from rest_framework.test import APITestCase, APIClient
from .models import User
from oauth2_provider.models import Application


class TestUser(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_empty_user_list(self):
        """
        Test if the user list is empty
        :return: []
        """
        response = self.client.get(path='/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_add_new_user(self):
        """
        Test the addition of a new user to the table
        :return:
        """
        data = {
            'name': 'Michael',
            'role': 'CUSTOMER',
            'email': 'allwin@gmail.com'
        }
        response = self.client.post(path='/user/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], data['email'])

    def test_incorrect_data(self):
        """
        Test validation errors
        :return: Validation error message with the missing fields
        """
        data = {
            'name': 'John'
        }
        response = self.client.post(path='/user/', data=data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(str(response.data['email']),
                         "[ErrorDetail(string='This field is required.', code='required')]")

    def test_user_list_after_adding_records(self):
        """
        Test if the newly added recorded data is returned
        :return:
        """
        data = {
            'name': 'Michael',
            'role': 'CUSTOMER',
            'email': 'allwin@gmail.com'
        }
        response = self.client.post(path='/user/', data=data)

        self.assertEqual(response.status_code, 201)
        response = self.client.get(path='/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class TestAccessToken(APITestCase):
    def setUp(self) -> None:
        pass

    def test_invalid_user(self):
        """
        Try to get access token for an invalid login credential
        :return: 401, Invalid login credentials
        """
        data = {
            "email": "abc@gmail.com",
            "password": "123456"
        }
        response = self.client.post(path='/user/token/', data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'Invalid Login Credentials!')

    def test_valid_user(self):
        data = {
            "email": "abc@gmail.com",
            "password": "123456",
            "role": User.AUTHOR
        }
        user = User.objects._create_user(**data)
        application = Application(
            name="Authorization",
            client_type="confidential",
            authorization_grant_type="password",
            user_id=user.pk
        )
        application.save()

        response = self.client.post(path='/user/token/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('access_token' in response.data.keys())
