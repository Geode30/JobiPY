from django.urls import path, re_path

from . import views,api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('setup', views.setup, name='setup'),
    path('jobs', views.jobs, name='jobs'),
    path('post', views.post, name='post'),
    path('profile', views.profile, name='profile'),
    path('message/<str:group_name>', views.message, name='message'),
    path('posted', views.posted, name='posted'),
    
    # API Routes
    
    path("api/register", api_views.api_register, name='api_register'),
    path("api/login/<str:email>/<str:password>", api_views.api_login, name='api_login'),
    path("api/setup", api_views.api_setup, name='api_setup'),
    path("api/post", api_views.api_post, name='api_post'),
    path("api/user", api_views.api_get_user, name='api_user'),
    path("api/logout", api_views.api_logout, name='api_logout'),
    path("api/jobs", api_views.api_jobs, name='api_jobs'),
    path("api/preferences", api_views.api_get_preferences, name='api_preferences'),
    path("api/replace/resume", api_views.api_replace_resume, name='api_resume'),
    path("api/apply", api_views.api_apply, name='api_apply'),
    path("api/posted", api_views.api_posted, name='api_posted'),
    path("api/resume/<int:id>", api_views.api_resume, name='api_resume_name'),
    path("api/group", api_views.api_group_name, name='api_group_name'),
    path("api/conversation", api_views.api_conversation, name='api_conversation'),
    path("api/retrieve/conversation/group/<str:group_name>", api_views.api_retrieve_conversation_group, name='api_retrieve_conversation_group'),
    path("api/retrieve/conversation/id/<int:id>", api_views.api_retrieve_conversation_id, name='api_retrieve_conversation_id'),
    re_path(r'^api/search/(?P<job_title>[^/]+)(?:/(?P<city>[^/]+))?/$', api_views.api_search, name='api_search'),
]
