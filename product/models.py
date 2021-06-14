from django.db import models

# Create your models here.
from django.contrib.admin.options import ModelAdmin
from django.db import models
from django.db.models.aggregates import Avg, Count
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.urls import reverse
from account.models import User
from django.utils import timezone
import math
# Create your models here.


class Category(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    title = models.CharField(max_length=200, blank=False,
                             unique=True, primary_key=True)
    keywords = models.CharField(max_length=30)
    description = models.TextField(max_length=225)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_category_slug(self):
        return reverse('category_slug', kwargs={'slug': self.slug})


class Product(models.Model):
    STATUS = (('True', 'True'),

              ('False', 'False'), )

    category = models.ForeignKey(
        Category,  on_delete=models.CASCADE)
    title = models.CharField(max_length=100,)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_product_slug(self):
        return reverse('product_slug', kwargs={'slug': self.slug})

    @property
    def avaragereview(self):
        reviews = Comment.objects.filter(product=self).aggregate(avarage=Avg('rate'))
        avg=0
        if reviews['avarage'] is not None:
            avg=float(reviews['avarage'])

        #For limited decimal place 
        return round(avg,1)

    @property
    def no_of_reviews(self):
        reviews=Comment.objects.filter(product=self).count()
        noreviews=0
        if reviews is not None:
            noreviews=reviews
        return noreviews


    # @property
    # def images(self):
    #     imageslist=Images.objects.filter(product=self)
    #     list=[]
    #     if list is not None:
    #         list.append(imageslist)
    #     return list
    


class Favorite(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='favorite')
    user = models.ManyToManyField(User,related_name='user_favorite', blank=True)
    isFavorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.count()} fab {self.product.title}'


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
    title = models.CharField(max_length=30)
    image = models.ImageField(blank=True, upload_to='images/', )

    def __str__(self):
        return self.title

 
class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),

        ('False', 'False'), )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    @property
    def get_total_likes(self):
        
        likes=self.likes.user.count()

        getLikes=0
        if likes is not None:
            getLikes=likes
        return getLikes


    
    @property
    def get_total_dislikes(self):
        
  
        dislikes=self.dislikes.user.count()

        getLikes=0
        if dislikes is not None:
            getLikes=dislikes
        return getLikes
     
     
    #Display human time (x days ago, or now)   
    @property
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.create_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
class Like(models.Model):
    comment= models.OneToOneField(Comment,related_name='likes',on_delete=models.CASCADE)
    user= models.ManyToManyField(User,related_name='user_likes', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment)
class Dislike(models.Model):
    comment= models.OneToOneField(Comment,related_name='dislikes',on_delete=models.CASCADE)
    user= models.ManyToManyField(User,related_name='user_dislikes',blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment)


class ProductSpecification(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productSpecification')
    point = models.CharField(max_length=250,blank=True, null=True)
    def __str__(self):
        return self.point
