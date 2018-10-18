from django.db import models
from django.utils.text import slugify
# Create your models here.  auth
from .utils import Preference as Pref
from django.shortcuts import reverse
# Create your models here. profile
import time
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
from pygments import lexers, highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from django.urls import reverse
from django.contrib import messages,auth


class Language(models.Model):
    name = models.CharField(max_length=100)
    lang_code = models.CharField(max_length=100, unique=True, verbose_name='Language Code')
    slug = models.SlugField(max_length=100, unique=True)
    mime = models.CharField(max_length=100, help_text='MIME to use when sending snippet as file.')
    file_extension = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def get_lexer(self):
        return lexers.get_lexer_by_name(self.lang_code)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('djangobin:trending_snippets', args=[self.slug])
#java		
def get_default_language():
    lang = Language.objects.get_or_create(
        name='Plain Text',
        lang_code='text',
        slug='text',
        mime='text/plain',
        file_extension='.txt',
    )

    return lang[0].id


class Author(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    default_language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                         default=get_default_language)
    default_exposure = models.CharField(max_length=10, choices=Pref.exposure_choices,
                                        default=Pref.SNIPPET_EXPOSURE_PUBLIC)
    default_expiration = models.CharField(max_length=10, choices=Pref.expiration_choices,
                                        default=Pref.SNIPPET_EXPIRE_NEVER)
    private = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('djangobin:profile', args=[self.user.username])

    def get_snippet_count(self):
        return self.user.snippet_set.count()

    def get_preferences(self):
        return {'language': self.default_language.id, 'exposure': self.default_exposure,'expiration': self.default_expiration}	



#Comment   total 

class Snippet(models.Model):
    
    Bank = models.CharField(max_length=200)
    Account = models.CharField(max_length=200)
    Comment = models.TextField(blank=True)
    Product_name = models.CharField(max_length=200)
    Price = models.IntegerField(default=0)
    exposure = models.CharField(max_length=10)
    slug = models.SlugField(help_text='Read only field. Will be filled automatically.')
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Cost = models.IntegerField(default=0)	
    hits = models.IntegerField(default=0, help_text='Read only field. Will be updated after every visit to snippet.')  

    def __str__(self):
        return self.Account 
    def __unicode__(self):
        return self.slug
    def get_absolute_url(self):
        return reverse('djangobin:snippet_detail', args=[self.slug])
    
    def save(self,*args, **kwargs):
        
         
        if not self.slug:
            self.slug = str(time.time()).replace(".", "")
        
        if not self.Bank:
            self.Bank = "Untitled"
        super(Snippet, self).save(*args, **kwargs)  # Call the "real" save() highlight. profile
        

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name'] 

    def __str__(self):
       return self.name

    def get_absolute_url(self):
        return reverse('djangobin:tag_list', args=[self.slug])

    def save(self, *args, **kwargs):        
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs) 
		
@receiver(post_save, sender=User)		
def create_author(sender, **kwargs):
    if kwargs.get('created', False):
        Author.objects.get_or_create(user=kwargs.get('instance'))
		
#CustomUserAdmin
class FlatPage(models.Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    enable_comments = models.BooleanField(default=False)
    template_name = models.CharField(max_length=70, blank=True)
    registration_required = models.BooleanField(default=False)
	
	
class Langu(models.Model):
    name = models.CharField(max_length=100)
    lang_code = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    mime = models.CharField(max_length=100, help_text='MIME to use when sending snippet as file.')
    file_extension = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def get_lexer(self):
        return lexers.get_lexer_by_name(self.lang_code)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('djangobin:trending_snippets', args=[self.slug])	
	
	
class Pos(models.Model):
    bank = models.CharField(max_length=200)
    cost = models.IntegerField()
    account = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    
    
    def __str__(self):
        return self.account
    def save(self, *args, **kwargs):
        self.account = slugify(self.account)
        super(Pos, self).save(*args, **kwargs)
    def get_absolute_url(self):
     return reverse('post_detail')
	 
