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
    
      # to show many image fields in product table 
    inlines = [ProductImageInline, ProductSpecificationsInline]
  
    # to Autofield function 
    prepopulated_fields = {'slug': ('title',)}

    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))


class CommentAdmin(admin.ModelAdmin):
    list_display=['product', 'user','comment','rate']

class FavoriteAdmin(admin.ModelAdmin):
    list_display=['product','no_of_users']

    def no_of_users(self, obj):
        return obj.user.count()

class LikeAdmin(admin.ModelAdmin):
    list_display=['comment','no_of_likes']
    
    def no_of_likes(self,obj):
        return obj.user.count()
class DislikeAdmin(admin.ModelAdmin):
    list_display=['comment','no_of_dislikes']
    
    def no_of_dislikes(self,obj):
        return obj.user.count()

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(ProductSpecification)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
