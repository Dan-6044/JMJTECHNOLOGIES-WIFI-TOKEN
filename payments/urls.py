from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
    path('', views.clientPage, name='clientPage'),
     path('add-plan/', views.add_plan, name='add_plan'),
     path("process_mpesa_payment/", views.process_mpesa_payment, name="process_mpesa_payment"),
     path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),

     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
