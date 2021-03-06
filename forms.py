from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .utils import Preference, get_current_user
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .utils import Preference as Pref, get_current_user
from .tasks import send_activation_mail
from django.template.defaultfilters import slugify
from .models import Snippet, Language, Author, Tag,Langu,Pos
from .tasks import send_activation_mail
#expiration get_current_user(request)


class SnippetForm(forms.ModelForm):    
    
    
    class Meta:
        model = Snippet
        fields = ('Cost', 'Account','Bank',)
    def save(self,request):
        Snippet = super(SnippetForm, self).save(commit=False)
        Snippet.user = get_current_user(request)
        		
        Snippet.save()
        return Snippet 
#if request.user.is_authenticated:  posts = Snippet.objects.all().order_by("-id") QuerySet filter

class FormSnippet(forms.ModelForm):    
    
    
    class Meta:
        model = Snippet
        fields = ('Bank', 'Account','Cost','Comment', 'Price','Product_name')
    def __init__(self, request, *args, **kwargs):
        super(FormSnippet, self).__init__(*args, **kwargs)
        
        
    def clean_email(self):
        Bank = self.cleaned_data['Bank']
        if not Bank:
            raise ValidationError("This field is required.")
        if Snippet.objects.filter(Bank=self.cleaned_data['Bank']).count():
            raise ValidationError("Bank is taken.")
        return self.cleaned_data['Bank']        
           
					
    def save(self,request):
        
        Snippet = super(FormSnippet, self).save(commit=False)
        Snippet.user = get_current_user(request)
        		
        #Snippet.Price = self.cleaned_data['Cost']-self.cleaned_data['Price']         
        Snippet.Cost = self.cleaned_data['Cost']-self.cleaned_data['Price']
        		
        Snippet.save()
        return Snippet		
    
    		

       	
         
   	
          
#instances


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Langu
        fields = '__all__'        

    def clean_name(self):
        name = self.cleaned_data['name']
        name_l = name.lower()
        if name == 'djangobin' or name == 'DJANGOBIN':
            raise ValidationError("name can't be {}.".format(name))
        return name

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean(self):
        cleaned_data = super(LanguageForm, self).clean()
        slug = cleaned_data.get('slug')
        mime = cleaned_data.get('mime')

        if slug == mime:
            raise ValidationError("Slug and MIME shouldn't be same.")

        # Always return the data
        return cleaned_data	
		
		
class PostFor(forms.ModelForm):    
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)
    
    class Meta:
        model = Pos
        fields = ('bank', 'cost', 'account',)
    def save(self,request):
        Pos = super(PostFor, self).save(commit=False)
        Pos.author = get_current_user(request)
        Pos.save()
        return Pos	
        
#UserCreationForm
class ContactForm(forms.Form):
    BUG = 'b'
    FEEDBACK = 'fb'
    NEW_FEATURE = 'nf'
    OTHER = 'o'
    purpose_choices = (
        (FEEDBACK, 'Feedback'),
        (NEW_FEATURE, 'Feature Request'),
        (BUG, 'Bug'),
        (OTHER, 'Other'),
    )

    name = forms.CharField()
    email = forms.EmailField()
    purpose = forms.ChoiceField(choices=purpose_choices)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))

    def __init__(self, request, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if request.user.is_authenticated:
            self.fields['name'].required = False
            self.fields['email'].required = False

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("This field is required.")
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise ValidationError("Email is taken.")
        return self.cleaned_data['email']

    def save(self, request):

        user = super(CreateUserForm, self).save(commit=False)
        user.is_active = False
        user.save()

        context = {
            # 'instance': settings.DEFAULT_FROM_EMAIL,
            'request': request,
            'protocol': request.scheme,
            'username': self.cleaned_data.get('username'),
            'domain': request.META['HTTP_HOST'],
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }

        subject = render_to_string('djangobin/email/activation_subject.txt', context)
        email = render_to_string('djangobin/email/activation_email.txt', context)

        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user	
		
class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Search'}))
    mysnippet = forms.BooleanField(required=False)


	