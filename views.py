from django.core.mail import mail_admins
import datetime
from django.db.models import Q
from .forms import SnippetForm,LanguageForm,PostFor,ContactForm,LoginForm, CreateUserForm,SearchForm,FormSnippet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import template
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django_project import helpers
from django.shortcuts import (HttpResponse, render, redirect,get_object_or_404, reverse, get_list_or_404, Http404)

from django.contrib import messages,auth
from .models import Language, Snippet, Tag,Langu,Pos
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import paginate_result
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .decorators import private_snippet
from django.contrib.flatpages.models import FlatPage
from .utils import Preference as Pref, get_current_user
from django.forms.formsets import formset_factory
#forms  snippet_detail if request.user.is_authenticated:  name = f.cleaned_data['name'] is_authenticated = Author.objects.get(user__username='staff')
		
        
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
    return render(request, 'djangobin/index.html', {'form': f}) 	

	
def today_is(request):
    now = datetime.datetime.now()
    return render(request, 'djangobin/datetime.html', {
                                    'now': now,
                                    'template_name': 'djangobin/nav.html' ,
                                    'base_dir': settings.BASE_DIR }
                                )

#recent_snippet								

	

def book_category(request, category='sci-fi'):
    return HttpResponse("<p>Books in {} category</p>".format(category))

def extra_args(request, arg1, arg2):
    return HttpResponse("<p>arg1: {} <br> arg2: {} </p>".format(arg1, arg2))



def raw_snippet(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    return HttpResponse(snippet.original_code, content_type=snippet.language.mime)	
	
	

def download_snippet(request,snippet_Bankl):
    url ="http://localhost:8000/15378008331564682/"
    
    snippet = get_object_or_404(Snippet, slug=snippet_Bankl)
    file_extension = snippet.Bank
    filename = snippet.slug + file_extension
    res = HttpResponse(url)
    res['content-disposition'] = 'attachment; filename='
    return res
	

#Author

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

    # logged in user is same as the user being recent_snippet
    # show everything
    else:
        snippet_list = user.snippet_set.all()

    snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/profile.html',
                  {'user' : user, 'snippets' : snippets } )

				


def snippet_detail(request, snippet_slug):
    recent_snippet = Snippet.objects.all()[:8]
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    snippet.hits += 1
    snippet.save()
    return render(request, 'djangobin/snippet_detail.html', {'snippet': snippet, 
                                                             })	

def trending_snippets(request, language_slug=''):
    lang = None
    snippets = Snippet.objects
    if language_slug:
        snippets = snippets.filter(language__slug=language_slug)
        lang = get_object_or_404(Language, slug=language_slug)

    snippet_list = get_list_or_404(snippets.filter(exposure='public').order_by('-hits'))
    snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/trending.html', {'snippets': snippets, 'lang': lang})
	
def post_detail(request, pk):
    recent_snippet = Pos.objects.get(pk=pk).all()[:3]
    
    return render(request, 'djangobin/post_detail.html', {'recent_snippet': recent_snippet})	

#feedback	
def post_list(request):
    if request.user.is_superuser:
        posts = Pos.objects.order_by("-id").all()
    else:
        posts = Pos.objects.filter(author__username=request.user.username).order_by("-id")
    posts = helpers.pg_records(request, posts, 5)

    return render(request, 'djangobin/post_list.html', {'posts': posts})

def post_delete(request, pk):
    post = get_object_or_404(Pos, pk=pk)
    post.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Post deleted')
    return redirect(next_page)
	
def Snippet_delete(request, pk):
    post = get_object_or_404(Snippet, pk=pk)
    post.delete()
    next_page = request.GET['next']
    messages.add_message(request, messages.INFO, 'Post deleted')
    return redirect(next_page)	

def post_update(request, pk):
    post = get_object_or_404(Pos, pk=pk)

    # If request is POST, create a bound form(form with post_list)
    if request.method == "POST":
        f = PostFor(request.POST, instance=post)

        # check whether form is valid or not
        # if the form is valid, save the data to the post_detail
        # and redirect the user back to the update post form

        # If form is invalid show form with errors form
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_post = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_post.author = author
                updated_post.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_post = f.save()
            # if user is not a superuser
            else:
                updated_post = f.save(request)
                
                updated_post.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Post updated')
            return redirect(reverse('djangobin:post_update', args=[post.id])) 

    # if request is GET the show unbound form to the CreateUserForm
    else:
        f = PostFor(instance=post)

    return render(request, 'djangobin/post_update.html', {'form': f, 'post': post})

def Snippet_list(request):
    if request.user.is_superuser:
      
        posts = Snippet.objects.filter(user__username=request.user.username,Product_name='')
    posts = helpers.pg_records(request, posts, 5)

    return render(request, 'djangobin/trending.html', {'snippets': posts})

	
	

def update_lang(request, pk):
    post = get_object_or_404(Snippet, pk=pk)

    # If request is POST, create a bound form(form with only)
    if request.method == "POST":
        f = SnippetForm(request.POST, instance=post)

        # check whether form is valid or not
        # if the form is valid, save the data to the post_detail
        # and redirect the user back to the update post form

        # If form is invalid show form with errors form filter
        if f.is_valid():
            # if author is not selected and user is superuser, then assign the post to the author named staff
            if request.POST.get('author') == "" and request.user.is_superuser:
                updated_post = f.save(commit=False)
                author = Author.objects.get(user__username='staff')
                updated_post.author = author
                updated_post.save()
                f.save_m2m()
            # if author is selected and user is superuser
            elif request.POST.get('author') and request.user.is_superuser:
                updated_post = f.save()
            # if user is not a superuser
            else:
                updated_post = f.save(request)
                
                updated_post.save()
                f.save_m2m()

            messages.add_message(request, messages.INFO, 'Post updated')
            return redirect(reverse('djangobin:update_lang', args=[post.id])) 

    # if request is GET the show unbound form to the QuerySet Snippet.objects.order_by("-id")[:3]
    else:
        f = SnippetForm(instance=post)

    return render(request, 'djangobin/update_lang.html', {'form': f, 'post': post})
#post.Price request.user.is_authenticated: posts = Snippet.objects.filter(user__username=request.user.username).order_by("-id")
#FormSnippet
def importe(request,pk):
    if request.user.is_superuser:
        
             posts = Snippet.objects.only('Cost').order_by("-id")[:1]
		
    post = get_object_or_404(Snippet, pk=pk)
    if request.method == 'POST':
        user_form = FormSnippet(request,request.POST)
        profile_form = SnippetForm(request.POST, instance=post)
        
		
        if user_form.is_valid():
             user_form.save(request)
            
            
             updated_post = user_form.save(request) 
             return redirect(reverse('djangobin:important', args=[post.id]))
            
             

    else:
        user_form = FormSnippet(request,instance=post)
        

    return render(request, 'djangobin/importe.html', {
      'form': user_form
        
    })

def important(request,pk):
    if request.user.is_superuser:
        
             posts = Snippet.objects.only('Cost').order_by("-id")[:1]

    return render(request, 'djangobin/important.html', {'posts': posts})	
	
def post_add(request):
    if request.method == "POST":
       f = PostFor(request.POST)

       if f.is_valid():
            new_post = f.save(request)
            
            new_post.save()
            f.save_m2m()

            messages.add_message(request, messages.INFO, 'Post added')
            return redirect(reverse('djangobin:post_list'))

    else:
        f = PostFor()
    return render(request, 'djangobin/post_add.html', {'form': f})
	
	

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
	
def login(request):
    if request.user.is_authenticated():
        return redirect('djangobin:admin_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user recent_snippet
            auth.login(request, user)
            return redirect(reverse('djangobin:admin_page'))

        else:
            messages.error(request, 'Error wrong username/password')

    return redirect('djangobin:admin_page')
	
@login_required
def logout(request):
    auth.logout(request)
    return render(request,'djangobin/logout.html')


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

            # if the user is logged in then search his update_lang
            if request.user.is_authenticated:
               qs2 = Snippet.objects.filter(Q(user=request.user),
                                            Q(Bank__icontains=query) | Q(Product_name__icontains=query))
               snippet_list = (qs1 | qs2).distinct()

            else:
                snippet_list = qs1

        snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/search.html', {'form': f, 'snippets': snippets })