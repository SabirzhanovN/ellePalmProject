from django.db import models


# Enum
class Size(models.Model):
    size = models.CharField(max_length=255, verbose_name="Размер")

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"
        ordering = ["size"]

    def __str__(self):
        return self.size


class Color(models.Model):
    color = models.CharField(max_length=255, verbose_name="Цвет")

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
        ordering = ["color"]

    def __str__(self):
        return self.color


# -------------------------------------------

class Catalog(models.Model):
    name = models.CharField(max_length=255, verbose_name="Каталог")
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to="catalog/%Y/%m/%d/", verbose_name="Фото")

    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталоги"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to="category/%Y/%m/%d/", verbose_name="Фото", null=True, blank=True)

    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name="Каталог")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f'{self.name} ({self.catalog})'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=255)
    price = models.IntegerField(verbose_name="Цена")
    is_exist = models.BooleanField(default=True, verbose_name="В наличии")
    date_of_public = models.DateTimeField(auto_now=True, verbose_name="Дата публикации")

    main_image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    image_1 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    image_2 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    image_3 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    image_4 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    image_5 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    sizes = models.ManyToManyField(Size, blank=True, verbose_name="Размер")
    colors = models.ManyToManyField(Color, blank=True, verbose_name="Цвет")

    class Meta:
        verbose_name = "Одежда"
        verbose_name_plural = "Одежда"

    def __str__(self):
        return self.name
