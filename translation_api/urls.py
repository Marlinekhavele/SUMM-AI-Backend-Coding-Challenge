from django.urls import  path
from .views import TranslationViewSet

urlpatterns = [
    path('translations/', TranslationViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('translations/<str:pk>/', TranslationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('translations/translate/', TranslationViewSet.as_view({
        'post': 'translate'
    })),
    path('translations/user/', TranslationViewSet.as_view({
        'get': 'user_translations'
    })),
]