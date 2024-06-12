from django.urls import path

from . import views

urlpatterns = [
    path('favorites/add_to_favorites/<int:id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/delete_from_favorites/<int:id>/', views.delete_from_favorites, name='delete_from_favorites'),
    path('favorites/favorites_list/', views.favorites_list, name='favorites_list'),

    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('edit_cart/', views.edit_cart, name='edit_cart'),
    path('delete_cart/<int:id>', views.delete_cart, name='delete_cart'),
    path('delete_all_cart/', views.delete_all_cart, name='delete_all_cart')
]