from django.urls import path, re_path

from . import views

from .api import (api_register, api_login, 
               api_setup, api_jobs, api_profile, 
               api_posted, api_post, api_message,
                api_activities ,api_overall)

urlpatterns = [
    # ========================== Page Routes ==========================
    
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('setup', views.setup, name='setup'),
    path('jobs', views.jobs, name='jobs'),
    path('activities', views.activities, name='activities'),
    path('post', views.post, name='post'),
    path('profile', views.profile, name='profile'),
    path('message/<str:group_name>', views.message, name='message'),
    path('posted', views.posted, name='posted'),
    
    # ========================== API Routes ==========================
    
    #register
    path("api/register", api_register.api_register, name='api_register'),
    
    #login
    path("api/login/<str:email>/<str:password>", api_login.api_login, name='api_login'),
    
    #setup or update preferences
    path("api/setup", api_setup.api_setup, name='api_setup'),
    path("api/preferences", api_setup.api_get_preferences, name='api_preferences'),
    
    #post
    path("api/post", api_post.api_post, name='api_post'),
    
    #activities
    path('api/activities', api_activities.api_applied_jobs, name='api_applied_jobs'),
    
    #APIs used every page
    path("api/user", api_overall.api_get_user, name='api_user'),
    path("api/logout", api_overall.api_logout, name='api_logout'),
    path('api/notification', api_overall.api_notification, name='api_notif'),
    path("api/message/read", api_overall.api_read, name='api_read'),
    path("api/application/status", api_overall.api_view_status, name='api_status'),
    
    #jobs
    path("api/jobs", api_jobs.api_jobs, name='api_jobs'),
    path("api/apply", api_jobs.api_apply, name='api_apply'),
    re_path(r'^api/search/(?P<job_title>[^/]+)(?:/(?P<city>[^/]+))?/$', api_jobs.api_search, name='api_search'),

    #profile    
    path("api/replace/resume", api_profile.api_replace_resume, name='api_resume'),
    
    #posted
    path("api/posted", api_posted.api_posted, name='api_posted'),
    path("api/resume/<int:id>/<int:job_id>", api_posted.api_view_resume, name='api_resume_name'),
    path("api/group", api_posted.api_group_name, name='api_group_name'),
    path("api/retrieve/conversation/id/<int:id>/<int:job_id>", api_posted.api_retrieve_conversation_id, name='api_retrieve_conversation_id'),
    path("api/conversation", api_posted.api_conversation, name='api_conversation'),    
    path("api/status/<int:user_id>/<int:job_id>/<str:status>", api_posted.api_set_status, name='api_set_status'), 
    
    #message
    path("api/message", api_message.api_message, name='api_message'),
    path("api/retrieve/conversation/group/<str:group_name>", api_message.api_retrieve_conversation_group, name='api_retrieve_conversation_group'),
]
