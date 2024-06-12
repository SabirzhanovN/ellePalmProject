from django.contrib import admin
from .models import Cart, Favorite, History


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'color', 'size', 'total_count', 'total_price')
    list_display_links = ('user',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_display_links = ('id',)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'address', 'total_price', 'total_count', 'date_of_create')