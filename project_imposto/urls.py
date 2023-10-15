from django.urls import path
from app_imposto import views

urlpatterns = [
    path(r'', views.tributacao, name='tributacao'),
    path('maioresImpostos', views.maioresImpostos, name='maioresImpostos'),
    path('impostometro', views.impostometro, name='impostometro')
]