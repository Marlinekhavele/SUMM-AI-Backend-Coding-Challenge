from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Translation
from .serializers import TranslationSerializer
from bs4 import BeautifulSoup
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import requests
import asyncio

class TranslationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows translations to be viewed or edited.
    """
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


    @action(detail=False, methods=['post'])
    def translate(self, request):
        """
        Translate the text in the request body.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        original_text = serializer.validated_data['original_text']
        content_type = serializer.validated_data['content_type']

        if content_type == 'html':
            translated_text = self.translate_html(original_text)
        else:
            translated_text = self.translate_text(original_text)
        # Update the validated data with the translated text
        serializer.validated_data['translated_text'] = translated_text

        # Save the translation
        translation = serializer.save()

        return Response(TranslationSerializer(translation).data, status=status.HTTP_201_CREATED)

    def translate_html(self, html):
        """
        Translate the text in the HTML document.
        """
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.find_all(text=True)
        
        async def translate_all():
            tasks = [asyncio.create_task(self.translate_text(text)) for text in texts if text.strip()]
            translated_texts = await asyncio.gather(*tasks)
            return translated_texts

        translated_texts = asyncio.run(translate_all())

        for original, translated in zip(texts, translated_texts):
            if original.strip():
                original.replace_with(translated)

        return str(soup)

    async def translate_text(self, text):
        """
        Translate the text using a Google translate.
        """

        # Here you would integrate with a third-party translation API
        # For this example, we'll just return the original text
        return text

    @action(detail=False, methods=['get'])
    def user_translations(self, request):
        translations = Translation.objects.filter(user=request.user)
        serializer = self.get_serializer(translations, many=True)
        return Response(serializer.data)