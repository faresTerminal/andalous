
from django import forms
from django.db import models
from tinymce.widgets import TinyMCE

from andalous.models import articles, booking, contact, author, Plat_a_manger, comment_put, happy_costumer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.db import models
from registration.forms import RegistrationForm


class TinyMCEWidget(TinyMCE):
  def use_required_attribute(self, *args):
     return False


# add multy fields to register page
class MyRegistrationForm(UserCreationForm):
   
   email = forms.EmailField(required = True)
  
  


   class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

   def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
       
        user.email = self.cleaned_data['email']
       

        if commit:
                user.save()
        return user 

   def clean_email(self):
      email = self.cleaned_data['email']
      qs = User.objects.filter(email = email)
      if qs.exists():
          raise ValidationError ('Email is already registed')
      return email


   def check_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")

        return email 


        
class createForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = articles
        fields = [
           
            'title',
            'image',
            'body',
          
          
        ]


class bookingForm(forms.ModelForm):

        class Meta:
                model = booking
                fields = [
                 'nom',
                 'email',
                 'phone',
                 'date',
                 'hour',
                 'person',
                 
                ]

class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_picture',
            
        ]

class contactForm(forms.ModelForm):

        class Meta:
                model = contact
                fields = [
                 'name',
                 'email',
                 'subject',
                 'message',
                 
                ]


class PlatForm(forms.ModelForm):

        class Meta:
            model = Plat_a_manger
            fields = [
               'title_plat',
               'price',
               'image_plat',

            ]

class CommentForm(forms.ModelForm):

        class Meta:
                model = comment_put
                fields =[
                 'comment',
                 
                ]
            

class createCostumerForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = happy_costumer
        fields = [
           
           
            'body',
          
          
        ]