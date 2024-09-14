from ..models import User, Conversation, Job_Application, Message
from django.http import JsonResponse
from datetime import datetime, timedelta

import json

def api_get_user(request):
    try:
        user = User.objects.get(id=request.session['user_id'])  
    except User.DoesNotExist:
        user = None
        
    if user is None:
        return JsonResponse({
            'message': 'User not found'
        })
    else:
        return JsonResponse({
            'message': 'Successful',
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'city': user.city,
            'contact_number':user.contact_number,
        })        

def api_logout(request):
    try:
        user = User.objects.get(id=request.session['user_id'])  
    except User.DoesNotExist:
        user = None
        
    if user is None:
        return JsonResponse({
            'message': 'User not found'
        })
    else:
        request.session['user_id'] = 0
        user.is_online = False
        user.save()
        return JsonResponse({
            'message': 'Logout Successfully',
        })

def api_notification(request):
    current_user = User.objects.get(id=request.session['user_id'])
    conversations = Conversation.objects.filter(people=current_user)
    
    messages = Message.objects.filter(is_read=False, receiver=current_user).select_related('conversation')

    distinct_conversations = messages.values('conversation').distinct()

    convo_count = distinct_conversations.count()
    
    applications = Job_Application.objects.filter(applicant=current_user).exclude(status='NotViewed')

    viewed_applications = Job_Application.objects.filter(applicant=current_user, status_viewed=False).exclude(status='NotViewed')

    all_messages = []
    status_notif = []

    for application in applications.all().order_by('date_applied'):
        _ = {
            'job_id': application.job.id,
            'company': application.job.company,
            'status': application.current_status(),
            'status_viewed': application.status_viewed,
            'application_id': application.id
        }
        status_notif.append(_)
    
    for _convo in conversations.all().order_by('-updated'):
        recent_message = Message.objects.filter(conversation=_convo).order_by('-date').first()
        
        if recent_message:
            sender = {
                'id': recent_message.sender.id,
                'name': _convo.job.company if _convo.job.poster.id != current_user.id else recent_message.sender.name,
            }
            
            _ = {
                'sender': sender,
                'id': _convo.id,
                'group_name': _convo.group_name,
                'message': recent_message.message,
                'time': get_time_difference(recent_message.date),
                'is_read': recent_message.is_read
            }
            
            all_messages.append(_)
    
    return JsonResponse({
        'message': 'Success',
        'message_notification': {
            'notif_count': convo_count,
            'all_messages': all_messages
            },
        'status_notification': {
            'notif_count': viewed_applications.count(),
            'notifications': status_notif
            }
    })

def api_read(request):
    user = User.objects.get(id=request.session['user_id'])
    data = json.loads(request.body)
    conversation_id = data['id']
    conversation = Conversation.objects.get(id=conversation_id)
    messages = Message.objects.filter(conversation=conversation, is_read=False, receiver=user).order_by('date')
    
    for message in messages.all():
        _message = Message.objects.get(id=message.id) 
        _message.is_read = True
        _message.save()
            
    return JsonResponse({
        'message': 'Messages Read'
    })

def api_view_status(request):
    current_user = User.objects.get(id=request.session['user_id'])   
    applications = Job_Application.objects.filter(applicant=current_user, status_viewed=False).exclude(status='NotViewed')
    for application in applications.all():
        application.status_viewed = True
        application.save()
    
    return JsonResponse({
        'message': 'Successful'
    })

def get_time_difference(given_date_str):
    date_format = "%B %d, %Y, %I:%M:%S %p"
    given_date = datetime.strptime(given_date_str, date_format)
    current_date = datetime.now()
    time_difference = current_date - given_date

    if time_difference <= timedelta(hours=1):
        return f"{int(time_difference.total_seconds() // 60)}m"
    elif time_difference <= timedelta(days=1):
        return f"{int(time_difference.total_seconds() // 3600)}h"
    else:
        return f"{int(time_difference.days)}d"

def display_resume_img(id):
    user = User.objects.get(id=id)
    image_path = user.resume_image

    return image_path