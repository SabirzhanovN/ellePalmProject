from django.contrib import admin
from django.utils.safestring import mark_safe

from . models import Size, Color, Catalog, Category, Product

admin.site.register(Size)
admin.site.register(Color)


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image_show')
    list_display_links = ('id',)
    list_editable = ('name',)
    list_per_page = 8
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def image_show(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width=60px />'.format(obj.image.url))
        return None


admin.site.register(Catalog, CatalogAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image_show', 'catalog')
    list_display_links = ('id',)
    list_editable = ('name',)
    list_per_page = 8
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}

    def image_show(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width=60px />'.format(obj.image.url))
        return None


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'price', 'is_exist', 'date_of_public', 'image_show', 'category')
    list_display_links = ('id',)
    list_editable = ('name', 'price', 'is_exist')
    list_per_page = 8
    search_fields = ('name', 'price', 'category')

    prepopulated_fields = {'slug': ('name',)}

    def image_show(self, obj):
        if obj.main_image:
            return mark_safe('<img src="{}" width=60px />'.format(obj.main_image.url))
        return None


admin.site.register(Product, ProductAdmin)

