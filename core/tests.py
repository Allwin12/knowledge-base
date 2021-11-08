from rest_framework.test import APITestCase, APIClient


class TestCategory(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_empty_category_list(self):
        response = self.client.get(path='/base/category/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])
