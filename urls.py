from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.flatpages import views as flat_views
# Snippet_list = 'admin_page' important

urlpatterns = [
    url(r'^important/(?P<pk>[\d]+)/$', views.important, name='important'),
    url(r'^importe/(?P<pk>[\d]+)/$', views.importe, name='importe'),    
    url(r'^userdetails/$', views.user_details, name='user_details'),
    url('^contact/$', views.contact, name='contact'),
    url(r'^(?P<pk>[\d]+)/$', views.Snippet_delete, name='Snippet_delete'),
    url('^update-lang/(?P<pk>[\d]+)/$', views.update_lang, name='update_lang'),
    url(r'^trending/$', views.Snippet_list, name='Snippet_list'), 
    url('^(?P<snippet_slug>[\d]+)/$', views.snippet_detail, name='snippet_detail'),
    url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^eula/$', flat_views.flatpage, {'url': '/eula/'}, name='eula'),
    url(r'^pp/$', views.post_detail, name='post_detail'),
	
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/add/$', views.post_add, name='post_add'),
    url(r'^post/update/(?P<pk>[\d]+)/$', views.post_update, name='post_update'),
    url(r'^post/delete/(?P<pk>[\d]+)/$', views.post_delete, name='post_delete'),
	
    url(r'^time/$', views.today_is, name='time'),
    url(r'^$', views.index, name='index'),
    
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
    
    url('^trending/', views.trending_snippets, name='trending_snippets'),
    
    url('^download/(?P<snippet_Bankl>[\d]+)/$', views.download_snippet, name='download_snippet'),
    url('^raw/(?P<snippet_slug>[\d]+)/$', views.raw_snippet, name='raw_snippet'),    
    
    url(r'^books/$', views.book_category, name='book_category'),
    url(r'^books/(?P<category>[\w-]+)/$', views.book_category, name='book_category'),
    url(r'^extra/$', views.extra_args, name='extra_args'),
    # password reset password_reset_confirm

    url('^password-reset/$', auth_views.password_reset,
        {'template_name': 'djangobin/password_reset.html',
         'email_template_name': 'djangobin/email/password_reset_email.txt',
         'subject_template_name': 'djangobin/email/password_reset_subject.txt',
         'post_reset_redirect': 'djangobin:password_reset_done',
        },
        name='password_reset'),

    url('^password-reset-done/$', auth_views.password_reset_done,
        {'template_name': 'djangobin/password_reset_done.html',},
        name='password_reset_done'),

    url(r'^password-confirm/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'djangobin/password_reset_confirm.html',
         'post_reset_redirect': 'djangobin:password_reset_complete'},
        name='password_reset_confirm'),

    url(r'password-reset-complete/$',
        auth_views.password_reset_complete,
        {'template_name':
             'djangobin/password_reset_complete.html'},
        name='password_reset_complete'),
    
    url(r'^login/$',auth_views.login, {'template_name': 'djangobin/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'djangobin/logout.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/'r'(?P<uidb64>[0-9A-Za-z_\-]+)/'r'(?P<token>[0-9A-Za-z]{1,13}'r'-[0-9A-Za-z]{1,20})/$',
     views.activate_account, name='activate'),	
	#password_reset_done
    # password user_details login

    url(r'^password-change/$', auth_views.password_change,
        {'template_name': 'djangobin/password_change.html',
        'post_change_redirect': 'djangobin:password_change_done'},
        name='password_change'
        ),

    url(r'^password-change-done/$', auth_views.password_change_done,
        {'template_name': 'djangobin/password_change_done.html'},
        name='password_change_done'
        ),
    url('^search/$', views.search, name='search'),
    url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^eula/$', flat_views.flatpage, {'url': '/eula/'}, name='eula'),
    url('^admin_page/$', views.admin_page, name='admin_page'),	
    
]