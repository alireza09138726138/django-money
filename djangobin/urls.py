from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.flatpages import views as flat_views
from django.views.generic import TemplateView
# Snippet_list = 'hello' 

urlpatterns = [
    
    url(r'^seeproduc/$', views.seeproduc, name='seeproduc'),
    url(r'^seeproduct/$', views.seeproduct, name='seeproduct'),
    url(r'^seeyeard/$', views.seeyeard, name='seeyeard'),
    url(r'^searchhseed/$', views.searchhseed, name='searchhseed'),
    url(r'^seeyearm/$', views.seeyearm, name='seeyearm'),
    url(r'^searchhseem/$', views.searchhseem, name='searchhseem'),
    url(r'^seeyear/$', views.seeyear, name='seeyear'),
    url(r'^searchhsee/$', views.searchhsee, name='searchhsee'),
    url(r'^searchedi/$', views.searchedi, name='searchedi'),
    url(r'^edi/$', views.edi, name='edi'),
    url(r'^asdd/$', views.asdd, name='asdd'),
    url(r'^sear/$', views.sear, name='sear'),
    url(r'^costt/$', views.costt, name='costt'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^searchedit/$', views.searchedit, name='searchedit'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^asd/$', views.asd, name='asd'),
    url(r'^searchh/$', views.searchh, name='searchh'),
    url(r'^search_form/$', views.search_form, name='search_form'),
    #url(r'^cost/$', views.cost, name='cost'),    
    url(r'^userdetails/$', views.user_details, name='user_details'),
    url('^contact/$', views.contact, name='contact'),
    #url(r'^(?P<pk>[\d]+)/$', views.Snippet_delete, name='Snippet_delete'),
    url(r'^trending/$', views.Snippet_list, name='Snippet_list'), 
    url('^(?P<snippet_slug>[\d]+)/$', views.snippet_detail, name='snippet_detail'),
	
    url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^eula/$', flat_views.flatpage, {'url': '/eula/'}, name='eula'),
    url('^trending/', views.trending_snippets, name='trending_snippets'),
    url(r'^$', views.index, name='index'),
    
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),    
    
   
	
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
#post_add
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
    # password user_details password_reset

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