from . import views
from django.urls import path
urlpatterns = [
    path('', views.process_image, name='process_image'),
    path('gallery/', views.gallery, name='gallery')
]
