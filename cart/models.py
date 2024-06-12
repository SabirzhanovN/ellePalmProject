from django.db import models

from account.models import User
from shop.models import Product, Color, Size


class Cart(models.Model):
    # null для создания истории заказов, усли пользователь очистит корзину
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name='Цвет', null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер', null=True, blank=True)

    total_count = models.IntegerField(verbose_name="Количество")
    total_price = models.IntegerField(verbose_name="Стоимость")

    date_of_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{str(self.product)} ({str(self.product.category.name)}) | {str(self.size)} | {str(self.color)} | {str(self.total_count)}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранная"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return str(self.product)


class History(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500, null=True)
    delivery = models.CharField(max_length=50, null=True)
    date_of_create = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField(null=True)

    products = models.ManyToManyField(Cart, blank=True)

    total_count = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'

    def __str__(self):
        return f"Заказ № {str(self.id)}"

