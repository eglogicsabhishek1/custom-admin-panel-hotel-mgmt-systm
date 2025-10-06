from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='custom_admin_root'),  # Default route for custom_admin/
    path('login/', views.user_login, name='custom_login'),
    path('home/', views.home, name='home'),
    path('view/<str:model_name>/', views.view_model, name='view_model'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('edit/<str:model_name>/<int:pk>/', views.edit_model, name='edit_model'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_model, name='delete_model'),
    path('add/<str:model_name>/', views.add_model, name='add_model'),
    path('add_room/', views.add_room, name='add_room'),
]
