from django.shortcuts import render, Http404, get_object_or_404, redirect, HttpResponse, reverse
from andalous.models import articles, Category, Plat_a_manger,  booking, contact, author, comment_put, happy_costumer
from django.contrib import messages
from django.template.context_processors import csrf
from andalous.forms import bookingForm, contactForm, createAuthor, PlatForm, CommentForm, MyRegistrationForm, createCostumerForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response 
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decimal import *
from cart.forms import CartAddProductForm
from django.shortcuts import render_to_response  
from urllib.parse import quote 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from andalous.forms import MyRegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
from django.template import loader
from django.template.defaultfilters import slugify



# Create your views here.
def calculate_cart_price(username):
    price_all = 0
    for obj in Plat_a_manger.objects.filter(user_plat=username):
        price_all += obj.price
   
    return price_all

#open login page
def login(request):

    c = {}
    c.update(csrf (request))
    return render_to_response('home/login.html', c)


# function to see if the username and password user there is in database        
def auth_views(request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        

        user  = auth.authenticate(username = username, password = password)

        if user is not None:
                auth.login(request, user)
                # when user have pic profile rederect loggedin page 
                user = get_object_or_404(User, id=request.user.id)
                author_profile = author.objects.filter(name=user.id)
                if author_profile:
                       authorUser = get_object_or_404(author, name=request.user.id)

                       messages.success(request, 'مرحبا بك ', extra_tags='welcome')
                       
                       return HttpResponseRedirect('/')

                # else rederect to chose pic profile
                else:
                           
                           return HttpResponseRedirect('/avatar')
               
                
              
                
        else: 
                
                messages.success(request, 'إسم المستخدم أو كلمة السر غير صحيحة', extra_tags='passwordWrong')
                return HttpResponseRedirect('/')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/')


# create register function
def register(request):
        
    form = MyRegistrationForm(request.POST or None)
    if form.is_valid():

        instance = form.save(commit=True)
        instance.is_active = False
        instance.save()
        site=get_current_site(request)
        mail_subject="Confirmation message for me"
        message=render_to_string('home/confirm_email.html',{
            'user':instance,
            'domain':site.domain,
            'uid':instance.id,
            'token':activation_token.make_token(instance)
        })
        to_email=form.cleaned_data.get('email')
        to_list=[to_email]
        from_email=settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, to_list, fail_silently=False)
     
        return HttpResponse("<h1>Thanks for your registration. A confirmation link was sent to your email</h1>")
     
    return render(request, 'home/register.html', {"form": form})


def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk = uid)
    except:
        raise Http404('No user faound')
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('<h1> Account is activated now you can <a href ="/login">login</a></h1>')
    else:
        return HttpResponse('<h3> Invalid activation Link </h3>')   



#chose avatar 
def avatar(request):
        return render(request, 'home/avatar.html')


def getProfile(request):
    if request.user.is_authenticated:

        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)

       
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = articles.objects.filter(avatar=authorUser.id).order_by('-id')

            paginator = Paginator(post, 10)

            page = request.GET.get('page')
            try:
              queryset = paginator.page(page)

            
            except PageNotAnInteger:
                queryset = paginator.page(1) 
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages) 

           


           
         
            return render(request, 'home/profile.html', {"user": authorUser, 'post':  queryset, 'full_name': request.user.username,})

        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.name = user
                ins.save()
                
                return HttpResponseRedirect('/')
            return render(request, 'home/avatar.html', {"form": form})

    else:
        return HttpResponseRedirect('/login')


def search(request): 
           all_articles = Plat_a_manger.objects.all().order_by('-id')
             # to search in loggedin page
           search = request.GET.get('q')
           if search:
              messages.success(request, 'تم البحث', extra_tags='search')
              all_articles = all_articles.filter(
                Q(title_plat__icontains=search) 
                

              )
            

           return render(request, 'home/search.html', {'all_articles': all_articles,})

# open home page
def index(request):

        # add pla to header
        plat = Plat_a_manger.objects.all().order_by('-id')[:4]
        # show menu
        menu = Plat_a_manger.objects.all().order_by('-id')[:6]
        # show blog
        blog = articles.objects.all().order_by('-id')[:3]
        customer = happy_costumer.objects.all().order_by('-id')

        context ={


         'plat':plat,
         'menu':menu,
         'blog':blog,
         'customer': customer,
         'full_name': request.user.username,
        }

         
        return render(request, 'home/index.html', context) 
        

# about page
def about(request):
        
       return render(request, 'home/about.html', {'full_name': request.user.username})


def contact(request):
        
        
       
        return render(request, 'home/contact.html', {'full_name': request.user.username})



def blog(request):
        post1 = articles.objects.all().order_by('-id')
          
           
        return render(request, 'home/blog.html', {'post1': post1, 'full_name': request.user.username})



# show the true link publish(details)
def show_article(request, id, slug):
      
    post = get_object_or_404(articles, id=id, slug = slug)
    add = comment_put.objects.all().filter(user_put = id).order_by('-id')

    art = articles.objects.get(pk = id, slug = slug)
    category = Category.objects.all().order_by('id')
 
    context = {
         'art': art,
         'add': add,
         'post': post,
         'category': category,
         'full_name': request.user.username,
        
          }

    return render(request, 'home/blog-single.html', context)






# make reservation

def booking(request):
   
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        f = bookingForm(request.POST or None)
        if f.is_valid():
            c = f.save(commit = False)
            c.user_booking = request.user
          
            c.save()

   
    messages.success(request,'Ton table est reservé, Pour plus d informations, appelez le numéro suivant: 021 21 26 20', extra_tags='bookingCM' )
    
    
    return HttpResponseRedirect('/')

def booking_page(request):

    return render(request, 'home/reservation.html')


# make reservation

def contact_as(request):
   
   
    if request.method == 'POST':
        f = contactForm(request.POST or None)
        if f.is_valid():
            c = f.save(commit = False)
           
          
            c.save()

   
    messages.success(request,'Votre message a été envoyé. Pour plus d informations, appelez le numéro du restaurant', extra_tags='contact10CM' )
    
    
    return HttpResponseRedirect('/contact')




# show user profile
def show_profile(request, id):
   
    
      
    post = get_object_or_404(author, id=id)
    
    art = articles.objects.filter(avatar=post.id).order_by('-id')
   
    
   
    context = {
       
         
         'art': art,
         'user': post,
         'full_name': request.user.username,
       
       
          }
   
  
    return render(request, 'home/profile_visited.html', context)



 

def product_list(request):

    category = None
   
    products = Plat_a_manger.objects.all()

    second = Plat_a_manger.objects.filter(available=True).filter(category = 2).order_by('id')[:10] #Entrées Froides
    four = Plat_a_manger.objects.filter(category = 3).order_by('id')[:10] # Entrées Chaudes
    five = Plat_a_manger.objects.filter(available=True).filter(category = 4).order_by('id')[:10] #Plats Traditionnels 
    six = Plat_a_manger.objects.filter(available=True).filter(category = 5).order_by('id')[:10]
    seven = Plat_a_manger.objects.filter(available=True).filter(category = 6).order_by('id')[:10]
    eight = Plat_a_manger.objects.filter(available=True).filter(category = 7).order_by('id')[:10]
    nane = Plat_a_manger.objects.filter(available=True).filter(category = 8).order_by('id')[:10]
    ten = Plat_a_manger.objects.filter(available=True).filter(category = 9).order_by('id')[:10]
    eleven = Plat_a_manger.objects.filter(available=True).filter(category = 10).order_by('id')[:10]

    ctx = {
             'products': products,
             'second': second,
             'four': four,
             'five': five,
             'six': six,
             'seven': seven,
             'eight': eight,
             'nane': nane,
             'ten': ten,
             'eleven': eleven,
             'full_name': request.user.username,
        }
    
    return render(request, 'home/menu.html', ctx)
                       
                      

def product_detail(request, id):
    product = get_object_or_404(Plat_a_manger,
                                         id=id,
                                        
                                         available=True)

    cart_product_form = CartAddProductForm()
    return render(request,
                    'home/plat_detail.html',
                    {'product': product,
                    'cart_product_form': cart_product_form})



# save comment user login in database comment_put

def save_comment(request, id):
   
    post = articles.objects.get(id = id)
    user = get_object_or_404(User, id=request.user.id)
    author_profile = author.objects.filter(name=user.id)
    authorUser = get_object_or_404(author, name=request.user.id)
   
    
    if request.method == 'POST':
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit = False)
            c.avatar_commenter = authorUser
            c.user_put = post
            c.user_comment = request.user
            c.save()

    add = comment_put.objects.all().order_by('-id')[:1]
    context = {
      'post': post,
      
      
      'add':add,
    
    }
    messages.success(request, 'votre commentaire à été publié', extra_tags='commentuser')
    
    redirect_to = reverse('andalous:show_article', kwargs={'id': post.id, 'slug': post.slug})
    return redirect(redirect_to, context)


# to pass to page to create one article     
def avis_customer(request):
    
       
        
    if request.user.is_authenticated:

        user = get_object_or_404(User, id=request.user.id)
        
        author_profile = author.objects.filter(name=user.id)

        # check if user has pic profile
        if author_profile:
          #if user has pic profile 
          form = createCostumerForm(request.POST or None, request.FILES or None)
          if form.is_valid():
           instance = form.save(commit = False)
           instance.save()
          return render(request, 'home/avis_costumer.html', {"form": form, 'full_name': request.user.username})
        # if user has not pic profile
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.name = user
                ins.save()
                
                return HttpResponseRedirect('/')
            return render(request, 'home/avatar.html', {"form": form})
    else:
      HttpResponseRedirect('/login')


def publish(request): 
       
        if request.user.is_authenticated:
          user = get_object_or_404(User, id=request.user.id)
          
          author_profile = author.objects.filter(name=user.id)
        
          authorUser = get_object_or_404(author, name=request.user.id)
          
    
          form = createCostumerForm (request.POST or None, request.FILES or None)
          

          if form.is_valid():
            
            instance = form.save(commit=False)
           
        # pass instance author
            instance.costumer_pic = authorUser
        # pass instance user login
            instance.coctumer = request.user
          

            instance.save()

        #pass from data base to template
            messages.success(request, 'Merci d avoir partagé votre avis', extra_tags='Done')
            redirect_to = reverse('andalous:index')
            return redirect(redirect_to)
          return render(request, 'home/index.html', {'form': form, 'user': authorUser, 'full_name': request.user.username})
         
        
        else:
          return HttpResponseRedirect('/login')