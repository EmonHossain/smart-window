from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('img/analysis/', views.image_analysis, name='image_analysis'),
    path('geoinfo/', views.current_geo_info, name='geo_information'),
]