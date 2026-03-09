from django.urls import path
from . import views

urlpatterns = [
    path('content-types/', views.content_types, name='content-types'),
    path('content/<str:content_type>/', views.get_content, name='get-content'),
]

