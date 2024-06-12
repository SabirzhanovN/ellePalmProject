from django.urls import path

from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('make_order/', views.make_order, name='make_order'),
    path('make_order/<int:id>/', views.make_order_single, name='make_order_single'),
    path('call_back/', views.call_back, name='call_back')
]

