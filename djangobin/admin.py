from django.contrib import admin
from . import models
# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'mime', 'created_on')
    search_fields = ['name', 'mime']
    ordering = ['name']
    list_filter = ['created_on']
    date_hierarchy = 'created_on'
	
class SnippetAdmin(admin.ModelAdmin):
    list_display = ( 'Price', 'exposure', 'user', 'Account', 'Bank')
    
    


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    # prepopulated_fields = {'slug': ('expiration',)}
    readonly_fields = ('slug',)


class AuthorInline(admin.StackedInline):
    model = models.Author


class CustomUserAdmin(UserAdmin):
    inlines = (AuthorInline, )    


admin.site.unregister(User) # unregister User model
admin.site.register(User, CustomUserAdmin) # register User model with changes
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Snippet, SnippetAdmin)
admin.site.register(models.Tag, TagAdmin)
