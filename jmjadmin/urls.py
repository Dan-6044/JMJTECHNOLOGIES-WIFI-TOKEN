from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [ 
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('add_station/', views.add_station, name='add_station'),
    path('view_station/', views.view_station, name='view_station'),
   path('edit_station/<int:id>/', views.edit_station, name='edit_station'),  # Edit station URL pattern
    path('delete_station/<int:id>/', views.delete_station, name='delete_station'),  # Delete station URL pattern
    
    
    
    
    path('hotspots/', views.hotspots, name='hotspots'),
    path('transactions/', views.transactions, name='transactions'),
    path('notifications/', views.notifications, name='notifications'),
    path('reports/', views.reports, name='reports'),
    path('analytics/', views.analytics, name='analytics'),
    path('billings/', views.billings, name='billings'),
    path('access_control/', views.access_control, name='access_control'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('logout/', views.logout_view, name='logout'),   

     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
