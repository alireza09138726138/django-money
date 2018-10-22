from django.core.mail import mail_admins
import datetime
from django.db.models import Q
from .forms import SnippetForm,ContactForm,LoginForm, CreateUserForm,SearchForm,FormSnippet,SnippetFormm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import template
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django_project import helpers
from django.shortcuts import (HttpResponse, render, redirect,get_object_or_404, reverse, get_list_or_404, Http404,render_to_response)

from django.contrib import messages,auth
from .models import Language, Snippet, Tag,Langu,Pos,Author
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import paginate_result
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .decorators import private_snippet
from django.contrib.flatpages.models import FlatPage
from .utils import Preference as Pref, get_current_user
from django.forms.formsets import formset_factory
#forms  snippet_detail if request.user.is_authenticated:  name = f.cleaned_data['name'] profile = Author.objects.get(user__username='staff')snippet_detail
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from datetime import timedelta,datetime

 #index        
def index(request):
    if request.method == "POST":
      f = SnippetForm(request.POST)
      if request.user.is_authenticated:
       posts = Snippet.objects.only('Price').order_by("-id")[:1]	  
       if f.is_valid():
        
            new_post = f.save(request)
            
            
            

            messages.add_message(request, messages.INFO, 'Post added')
            return redirect(reverse('djangobin:Snippet_list'))
      else:
         
         return redirect(reverse('djangobin:login'))
    else:
        f = SnippetForm()
    return render(request, 'djangobin/index.html', {'form': f,})


#search	
def search_form(request):
    return render(request,'djangobin/search_form.html')

#review of all buy according day
def searchhseed(request):
    errors = []
    if 'q' in request.GET:
     if request.user.is_authenticated:
        q = request.GET['q']
        q1 = request.GET['q1']
        books = Snippet.objects.filter(Bank=q,Account=q1).order_by("-id")[:1]
        return render(request,'djangobin/searchhseed.html',
                {'books': books, 'query': q, 'query1': q1})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})

	#review of all buy according day    this is continue of review of all buy according day 
def seeyeard(request):
    errors = []
    if request.GET:
     if request.user.is_authenticated:
        q = request.GET['Bank']
        q1 = request.GET['Account']
        yea = request.GET['yea']
        mont = request.GET['month']
        day = request.GET['day']
        books = Snippet.objects.filter(Product_name__gt='',Product_name__isnull=False,Bank=q,Account=q1,created_on__day=day,created_on__month=mont,created_on__year=yea,user=request.user).all  #,created_on__year=year 
		
        return render(request,'djangobin/seeyeard.html',
                {'books': books})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})	
	
	
	
#review of all buy according   month
def searchhseem(request):
    errors = []
    if 'q' in request.GET:
     if request.user.is_authenticated:
        q = request.GET['q']
        q1 = request.GET['q1']
        books = Snippet.objects.filter(Bank=q,Account=q1).order_by("-id")[:1]
        return render(request,'djangobin/searchhseem.html',
                {'books': books, 'query': q, 'query1': q1})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})

	
#this is continue of review of all buy according month	
def seeyearm(request):
    errors = []
    if request.GET:
     if request.user.is_authenticated:
        q = request.GET['Bank']
        q1 = request.GET['Account']
        yea = request.GET['yea']
        mont = request.GET['month']
        books = Snippet.objects.filter(Product_name__gt='',Product_name__isnull=False,Bank=q,Account=q1,created_on__month=mont,created_on__year=yea,user=request.user).all  #,created_on__year=year 
		
        return render(request,'djangobin/seeyearm.html',
                {'books': books})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})	

#review of all buy according   product
def seeproduct(request):
    errors = []
    if request.GET:
     if request.user.is_authenticated:
        q = request.GET['Bank']
        q1 = request.GET['Account']
        
        books = Snippet.objects.values('Product_name','Bank','Account').distinct().filter(Product_name__gt='',Product_name__isnull=False,Bank=q,Account=q1,user=request.user)  # 
		
        boo = Snippet.objects.values('Bank','Account').distinct().filter(user=request.user).all()		
        return render(request,'djangobin/seeproduct.html',
                {'books': books,'boo': boo})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})

#this is continue of review of all buy according product	
def seeproduc(request):  
    errors = []
    if request.GET:
     if request.user.is_authenticated:
        Bank = request.GET['Bank']
        Account = request.GET['Account']
        Product_name = request.GET['Product_name']  
        
        books = Snippet.objects.filter(Account=Account,Bank=Bank,Product_name=Product_name,user=request.user).all #,created_on__year=reset 
		
        return render(request,'djangobin/seeproduc.html',
                {'books': books})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})	
	
	
	
##this is continue of review of all buy according year
def searchhsee(request):
    errors = []
    if 'q' in request.GET:
     if request.user.is_authenticated:
        q = request.GET['q']
        q1 = request.GET['q1']
        books = Snippet.objects.filter(Bank=q,Account=q1).order_by("-id")[:1]
        return render(request,'djangobin/searchhsee.html',
                {'books': books, 'query': q, 'query1': q1})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})
	
#this is continue of review of all buy according year
def seeyear(request):
    errors = []
    if request.GET:
     if request.user.is_authenticated:
        q = request.GET['Bank']
        q1 = request.GET['Account']
        yea = request.GET['yea']
        books = Snippet.objects.filter(Product_name__gt='',Product_name__isnull=False,Bank=q,Account=q1,created_on__year=yea,user=request.user).all  #,created_on__year=year 
		
        return render(request,'djangobin/seeyear.html',
                {'books': books})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})

def searchh(request):
    errors = []
    if 'q' in request.GET:
     if request.user.is_authenticated:
        q = request.GET['q']
        q1 = request.GET['q1']
        books = Snippet.objects.filter(Product_name__gt='',Product_name__isnull=False,Bank=q,Account=q1).order_by("-id")[:10]
        return render(request,'djangobin/search_results.html',
                {'books': books, 'query': q, 'query1': q1})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})

#delete on trending.html
def asd(request):
 if 'q' in request.GET  :
    q = request.GET  ['q']
    q1 = request.GET  ['q1']
    user = request.GET  ['user']
    post = Snippet.objects.filter(Bank=q,Account=q1,user__username=user)
    post.delete()
    
    messages.add_message(request, messages.INFO, 'Post deleted')
    return redirect('djangobin:Snippet_list')   

#edit or  update on trending.html	
def searchedit(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        q1 = request.GET['q1']
        books = Snippet.objects.filter(Bank=q,Account=q1).order_by("-id")[:1]
        return render(request,'djangobin/update.html',
                {'books': books, 'query': q, 'query1': q1})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})	
#continue of before update	
def edit(request):
 if 'Bank' in request.GET  :
  if request.user.is_authenticated:
    Bank = request.GET  ['Bank']
    Account = request.GET  ['Account']
    Cost = request.GET  ['Cost']
    id = request.GET  ['id']
    
    post = Snippet.objects.filter(Account=Account,user=request.user).update(Bank=Bank)
    return redirect('djangobin:Snippet_list')
  return render(request, 'djangobin/trending.html')
  
  	

	
#update on trending.html for account and cost	
def searchedi(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        q1 = request.GET['q1']
        books = Snippet.objects.filter(Bank=q,Account=q1).order_by("-id")[:1]
        return render(request,'djangobin/updat.html',
                {'books': books, 'query': q, 'query1': q1})
    
    return render(request,'djangobin/search_form.html',{'errors': errors})
	
#continue of before update	
def edi(request):
 if 'Bank' in request.GET  :
  if request.user.is_authenticated:
    Bank = request.GET  ['Bank']
    Account = request.GET  ['Account']
    Cost = request.GET  ['Cost']
    
    
    post = Snippet.objects.filter(Bank=Bank,user=request.user).update(Account=Account,Cost=Cost)
   
    return redirect('djangobin:Snippet_list')
  return render(request, 'djangobin/trending.html')




#buy on trending.html	
	
def buy(request):
   errors = []
   if 'q' in request.GET:
    if request.user.is_authenticated:	
        q = request.GET['q']
        q1 = request.GET['q1']
        books = Snippet.objects.filter(Bank=q,Account=q1).order_by("-id")[:1]
        
        return render(request, 'djangobin/costt.html',
                {'books': books, 'query': q, 'query1': q1})
   
   return redirect(reverse('djangobin:Snippet_list'))
     

 
 #continue of before buy on trending.html        		
def costt(request):
 
  if request.method == 'POST':
        
        f = SnippetFormm(request.POST)
        if request.user.is_authenticated:
         
         user = request.POST.get('user')
         Bank = request.POST.get('Bank')
         Account = request.POST.get('Account')
         if f.is_valid():

            Price = f.cleaned_data.get('Price')
            Cost = f.cleaned_data.get('Cost')
            if Cost < Price:
                messages.add_message(request, messages.INFO, 'Dont Post:  your price more then cost..')
                return redirect(reverse('djangobin:Snippet_list'))
            else:
              f.save(request)
              messages.add_message(request, messages.INFO, 'Post added')  
              return redirect(reverse('djangobin:sear'))

        else:
            messages.error(request, 'Error wrong username/password')
  else:
        f = SnippetFormm()
    

  return render(request, 'djangobin/costt.html')

  
#delete  
def asdd(request):
 if request.GET  :
  if request.user.is_authenticated:
    Comment = request.GET  ['Comment']
    Product_name = request.GET  ['Product_name']
    user = request.GET  ['user']
    post = Snippet.objects.filter(Comment=Comment,Product_name=Product_name,user__username=request.user)
    post.delete()
    
    messages.add_message(request, messages.INFO, 'Post deleted')
    return redirect('djangobin:sear')

 #list review according buy                  
def sear(request):
  
    if request.user.is_authenticated:
       #get new enter to 24 hours
        posts = Snippet.objects.order_by('-id').values('Cost','Comment', 'Price','Product_name').distinct().filter(user__username=request.user.username,Product_name__gt='',Product_name__isnull=False,created_on__gte = datetime.now() - timedelta(days=1))    
    posts = helpers.pg_records(request, posts, 4)

    return render(request, 'djangobin/trend.html', {'snippets': posts})
  	
   
 		
 	


#snippets list

def trending_snippets(request, language_slug=''):
    lang = None
    snippets = Snippet.objects
    if language_slug:
        snippets = snippets.filter(language__slug=language_slug)
        lang = get_object_or_404(Language, slug=language_slug)

    snippet_list = get_list_or_404(snippets.filter(exposure='public').order_by('-hits'))
    snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/trending.html', {'snippets': snippets, 'lang': lang})


def profile(request, username):
    user = get_object_or_404(User, username=username)

    # if the profile is private and logged in user is not same as the user being trending_snippet,
    # show 404 error
    if user.profile.private and request.user.username != user.username:
        raise Http404

    # if the profile is not private and logged in user is not same as the user being viewed,
    # then only show public snippets of the user
    elif not user.profile.private and request.user.username != user.username:
        snippet_list = user.snippet_set.filter(exposure='public')
        user.profile.views += 1
        user.profile.save()

    # logged in user is same as the user being Snippet_delete
    # show everything
    else:
        snippet_list = user.snippet_set.all()

    snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/profile.html',
                  {'user' : user, 'snippets' : snippets } )

				

@private_snippet
def snippet_detail(request, snippet_slug):
    
    
    snippet = Snippet.objects.get(slug=snippet_slug)
    snippe = Snippet.objects.filter(Account=snippet.Account,Bank=snippet.Bank,slug=snippet_slug).only('Cost').all().order_by("-id")
    
    return render(request, 'djangobin/snippet_detail.html', {'snippet': snippet,'snippe': snippe, 
                                                             })	


def Snippet_list(request):
    
    if request.user.is_authenticated:
         
        posts = Snippet.objects.values('Bank','Account').distinct().filter(user__username=request.user.username)   
        posts = helpers.pg_records(request, posts, 10)

        return render(request, 'djangobin/trending.html', {'snippets': posts})

	


	
#contact us
def contact(request):
    if request.method == 'POST':
        f = ContactForm(request, request.POST)
        if f.is_valid():

            if request.user.is_authenticated:
                
                name = f.cleaned_data['name']
                email = f.cleaned_data['email']  

            subject = "You have a new Feedback from {}:<{}>".format(name, email)

            message = "Purpose: {}\n\nDate: {}\n\nMessage:\n\n {}".format(
                dict(f.purpose_choices).get(f.cleaned_data['purpose']),
                datetime.datetime.now(),
                f.cleaned_data['message']
            )

            mail_admins(subject, message)

            messages.add_message(request, messages.INFO, 'Thanks for submitting your feedback.')

            return redirect('djangobin:contact')

    else:
        f = ContactForm(request)

    return render(request, 'djangobin/contact.html', {'form': f})
	
#Reverse 
@login_required	
def user_details(request):    
    user = get_object_or_404(User, id=request.user.id)    
    return render(request, 'djangobin/user_details.html', {'user': user})	

def admin_page(request):
    if request.user.is_superuser:
        
        posts = Snippet.objects.filter(user__username=request.user.username).order_by("-id")
        posts = helpers.pg_records(request, posts, 5)

    return render(request, 'djangobin/admin_page.html', {'user': posts})
	
	
#logout
	
def login(request):
    if request.user.is_authenticated:
        return redirect('djangobin:profile', username=request.user.username)
    if request.method == 'POST':

        f = LoginForm(request.POST)
        if f.is_valid():

            user = User.objects.filter(email=f.cleaned_data['email'])

            if user:
                user = auth.authenticate(
                    username=user[0].username,
                    password=f.cleaned_data['password'],
                )

                if user:
                    auth.login(request, user)
                    return redirect( request.GET.get('next') or 'djangobin:index' )

            messages.add_message(request, messages.INFO, 'Invalid email/password.')
            return redirect('djangobin:login')

    else:
        f = LoginForm()

    return render(request, 'djangobin/login.html', {'form': f})	
	
 

	
@login_required
def logout(request):
    auth.logout(request)
    return render(request,'djangobin/logout.html')

#form
def signup(request):
    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save(request)
            messages.success(request, 'Account created successfully. Check email to verify the account.')
            return redirect('djangobin:signup')

    else:
        f = CreateUserForm()

    return render(request, 'djangobin/signup.html', {'form': f})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if (user is not None and default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, 'Account activated. Please login.')
    else:
        messages.add_message(request, messages.INFO, 'Link Expired. Contact admin to activate your account.')

    return redirect('djangobin:login')
	
	

#search
def search(request):
    f = SearchForm(request.GET)
    snippets = []

    if f.is_valid():

        query = f.cleaned_data.get('query')
        mysnippets = f.cleaned_data.get('mysnippet')

        # if mysnippet field is selected, search only logged in user's snippets
        if mysnippets:
            snippet_list = Snippet.objects.filter(
                Q(user=request.user),
                Q(Bank__icontains=query) | Q(Product_name__icontains=query)
            )

        else:
            qs1 = Snippet.objects.filter(
                Q(exposure='public'),
                Q(Bank__icontains = query) | Q(Product_name__icontains = query)
                # Q(user=request.user)
            )

            # if the user is logged in then search his password_reset
            if request.user.is_authenticated:
               qs2 = Snippet.objects.filter(Q(user=request.user),
                                            Q(Bank__icontains=query) | Q(Product_name__icontains=query))
               snippet_list = (qs1 | qs2).distinct()

            else:
                snippet_list = qs1

        snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/search.html', {'form': f, 'snippets': snippets })
	

	
