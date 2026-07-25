from django.urls import path
from . import views

urlpatterns = [
    path('enskripsyon/', views.enskripsyon, name='enskripsyon'),
    path('verifye-kod/', views.verifye_kod, name='verifye_kod'),
    path('koneksyon/', views.koneksyon, name='koneksyon'),
    path('dekonksyon/', views.dekonksyon, name='dekonksyon'),
    path('kou-yo/', views.lis_kou, name='lis_kou'),
    path('peman/', views.peman, name='peman'),
    path('detay-kou/<int:leson_id>/', views.detay_kou, name='detay_kou'),
    path('kou/<int:pk>/', views.detay_kou, name='detay_kou'),
]