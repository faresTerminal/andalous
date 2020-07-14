from django.db import models
from django.shortcuts import reverse, Http404
from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField
import hashlib

from django.utils import timezone 
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from sorl.thumbnail import ImageField
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date

# Create your models here.




class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, allow_unicode=True)
    
    
    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)



class author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank = True, upload_to = 'Avatar', default= 'Avatar/deafult-profile-image.png')
   
    def __str__(self):
        return self.name.username

    





class articles(models.Model):
    article_author = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(author, on_delete = models.CASCADE)
    title = models.CharField('العنوان', max_length=9500)
    slug = models.SlugField(max_length=9500, unique_for_date='publish', allow_unicode=True)
    image = models.ImageField('صورة مناسبة', upload_to = 'Images')
    body = HTMLField()
    posted_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    publish = models.DateTimeField(default=timezone.now) 
   
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
    
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)

        super(articles, self).save(*args, **kwargs)

    

    def get_absolute_url(self):
        return reverse('andalous:show_article', kwargs={'id':self.id, 'slug': self.slug})
  



class Plat_a_manger(models.Model):

    user_plat = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, max_length=200, on_delete=models.CASCADE)
    title_plat = models.CharField('العنوان', max_length=9500)
    price = models.DecimalField(max_digits=200, decimal_places=2, default=0.00)
    image_plat = models.ImageField('صورة مناسبة', upload_to = 'Images_Plat')
    available = models.BooleanField(default=True)


    def calculate_price(self):
        
        
            self.price = price

      
        # print(f"Price for {self.subtype} version of Sub is {self.price}")


    def __str__(self):
        return self.title_plat

    def get_absolute_url(self):
         return reverse('andalous:product_detail',
            args=[self.id])



class booking(models.Model):
    user_booking = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length = 500, blank = True, null = True)
    email = models.EmailField(max_length = 500, blank = True, null = True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    date = models.DateField(("Date"), default=date.today)
    hour = models.IntegerField()
    person = models.IntegerField()

    def __str__(self):
        return self.nom


class contact(models.Model):

     name = models.CharField(max_length = 500, blank = True, null = True)
     email = models.EmailField(max_length = 500, blank = True, null = True)
     subject = models.CharField(max_length = 500, blank = True, null = True)
     message = models.TextField()

     def __str__(self):
         return self.subject


class comment_put(models.Model):

    user_comment = models.ForeignKey(User, default = None, on_delete = models.CASCADE)
    user_put = models.ForeignKey(articles, on_delete = models.CASCADE)
    avatar_commenter = models.ForeignKey(author, on_delete = models.CASCADE)
    comment = models.TextField(max_length = 500)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
   
    def __str__(self):
        return self.comment


class happy_costumer(models.Model):

    coctumer = models.ForeignKey(User, default = None, on_delete = models.CASCADE)
   
    costumer_pic = models.ForeignKey(author, on_delete = models.CASCADE)
    body = HTMLField()
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.body


    def get_absolute_url(self):
         return reverse('andalous:index')
        
