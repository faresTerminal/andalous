from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views





from .import views

app_name="andalous"
urlpatterns = [
    # home page
    url(r'^$', views.index, name='index'),
      # about page
    url(r'about/$', views.about, name="about"),
    # contact page
    url(r'contact/$', views.contact, name="contact"),

    # blog page
    url(r'blog/$', views.blog, name="blog"),
     # to go to spicial id when click a link 
    url(r'article/(?P<id>\d+)/(?P<slug>[\w-]+)/$', views.show_article, name='show_article'),
     # Menu page
   
    #reservation 
    url(r'^booking/$', views.booking, name='booking'),
    #reservation page 
    url(r'^booking_page/$', views.booking_page, name='booking_page'),
    #contact_as
    url(r'^contact_as/$', views.contact_as, name='contact_as'),
    #search page
    url(r'^search/$', views.search, name='search'),
    #open login page
    url(r'^login/$', views.login, name = 'login'),
     #check login
    url(r'^auth/$', views.auth_views, name='auth_views'),
      #chose avatar
    url(r'avatar/$', views.avatar, name='avatar'),

    url(r'profile/$', views.getProfile, name="getProfile"),
    # TO SHOW PROFILE
    url(r'user/(?P<id>\d+)/$', views.show_profile, name='show_profile'),
    url(r'menu/$', views.product_list, name="product_list"),
  
    path('<int:id>/', views.product_detail,
                name='product_detail'),
    url(r'add_comment/(?P<id>\d+)/$', views.save_comment, name='save_comment'),
    path("logout", views.logout_view, name="logout_view"),
    #open register page
    url(r'^register/$', views.register, name = 'register'),
    # create post
    url(r'create/$', views.avis_customer, name='avis_customer'),
     #publish
    url(r'publish/$', views.publish, name='publish'),
 

    
  
     #account confirmations
    path('activate/<uid>/<token>', views.activate, name="activate"),
 

   
    
]