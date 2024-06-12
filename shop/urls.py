from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/<str:slug>/', views.listing_products_by_catalog, name='listing_products_by_catalog'),
    path('catalog/<str:catalog>/<str:category>/', views.listing_products_by_category, name='listing_products_by_category'),
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
]
