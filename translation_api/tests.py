from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from .models import Translation

# Create your tests here.


class TranslationAPITestCase(TestCase):
    """
    Test cases for the Translation API.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test123', password='pass@123')
        self.client.force_authenticate(user=self.user)
        self.translation_url = '/api/translations/translate/'

    @patch('translation_api.views.openai')
    def test_successful_translation(self, mock_openai):
        """
        Test a successful translation request.
        """
        # Mock the OpenAI client response
        mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = "Bonjour, monde!"

        data = {
            'original_text': 'Hello, world!',
            'target_language': 'French',
            'content_type': 'text'
        }
        response = self.client.post(self.translation_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['translated_text'], 'Bonjour, monde!')
        self.assertEqual(Translation.objects.count(), 1)

    def test_missing_original_text(self):
        data = {
            'target_language': 'French',
            'content_type': 'text'
        }
        response = self.client.post(self.translation_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_target_language(self):
        data = {
            'original_text': 'Hello, world!',
            'target_language': 'InvalidLanguage',
            'content_type': 'text'
        }
        response = self.client.post(self.translation_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('translation_api.views.openai')
    def test_openai_api_error(self, mock_openai):
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")

        data = {
            'original_text': 'Hello, world!',
            'target_language': 'French',
            'content_type': 'text'
        }
        response = self.client.post(self.translation_url, data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_unauthenticated_request(self):
        self.client.force_authenticate(user=None)
        data = {
            'original_text': 'Hello, world!',
            'target_language': 'French',
            'content_type': 'text'
        }
        response = self.client.post(self.translation_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)