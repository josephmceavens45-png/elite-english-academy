from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('enskripsyon/', views.enskripsyon, name='enskripsyon'),
    path('koneksyon/', views.koneksyon, name='login'),
    path('koneksyon-alt/', views.koneksyon, name='koneksyon'),
    path('dekoneksyon/', views.dekoneksyon, name='dekoneksyon'),
    path('kou-yo/', views.lis_kou, name='lis_kou'),
    path('devwa/<int:devwa_id>/soumet/', views.soumet_devwa, name='soumet_devwa'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
