import unittest
from django.test.client import Client

class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://127.0.0.1:8000/books/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('http://127.0.0.1:8000/cuser/signin/')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'cuser/signin.html')

if __name__ == '__main__':
    unittest.main()