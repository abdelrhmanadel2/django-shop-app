from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']
    prepopulated_fields = {'slug': ('title',)}


class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class ProductSpecificationsInline(admin.TabularInline):
    model = ProductSpecification
    extra= 5


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'price',  'image_tag', 'category', 'status']
    list_filter = ['category']
    inlines = [ProductImageInline, ProductSpecificationsInline]
    # to view image in admin panel
    prepopulated_fields = {'slug': ('title',)}

    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))


class CommentAdmin(admin.ModelAdmin):
    list_display=['product', 'user','comment','rate']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(ProductSpecification)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite)
admin.site.register(Like)
admin.site.register(Dislike)
