from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Translation
from .serializers import TranslationSerializer
from bs4 import BeautifulSoup
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import openai
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

class TranslationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user translations.
    """
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @action(detail=False, methods=['post'])
    def translate(self, request):
        """
        Translate the given text to English
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        original_text = serializer.validated_data['original_text']
        content_type = serializer.validated_data.get('content_type', 'text')
        target_language = serializer.validated_data.get('target_language', 'English')

        if content_type == 'html':
            translated_text = self.translate_html(original_text, target_language)
        else:
            translated_text = self.translate_text(original_text, target_language)

        # Save translation
        serializer.validated_data['translated_text'] = translated_text
        translation = serializer.save()

        # Prepare response data
        response_data = {
            'original_text': original_text,
            'translated_text': translated_text,
            'target_language': target_language,
            'content_type': content_type
        }
        # save translation data for the response
        response_data = self.get_serializer(translation).data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def translate_text(self, text, target_language):
        """
        Translate the given text to the target language using GPT4.
        """
        try:
            response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
              messages=[
                {"role": "system", "content": f"Translate the following text to {target_language}. Only provide the translation."},
                {"role": "user", "content": text}
            ])
            translated_text = response.choices[0].message['content'].strip()
            logger.info(f"Received translation: '{translated_text}'")
            return translated_text
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails

    def translate_html(self, html, target_language):
        """
        Translate the text in the given HTML to the target language.
        """
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.find_all(text=True)
        
        for text in texts:
            if text.strip():
                translated = self.translate_text(text, target_language)
                text.replace_with(translated)

        return str(soup)

        
    @action(detail=False, methods=['get'])
    def user_translations(self, request):
        """
        Get the translations of the current user.
        """
        translations = Translation.objects.filter(user=request.user)
        serializer = self.get_serializer(translations, many=True)
        return Response(serializer.data)