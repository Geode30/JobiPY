from ..models import User, Job_Post, Conversation, Job_Application
from django.http import JsonResponse
import json
import random
import string

def api_posted(request):
    user = User.objects.get(id=request.session['user_id'])
    posted_jobs = Job_Post.objects.filter(poster=user).order_by('-date_posted')
    
    job_list = []
    
    for job in posted_jobs:
        users = []
        
        applications = Job_Application.objects.filter(job=job)
        for application in applications:
            __user = {
                'id': application.applicant.id,
                'name': application.applicant.name
            }
            users.append(__user)
        
        _job = {
            'id': job.id,
            'poster': job.poster.name,
            'job_title': job.job_title,
            'company': job.company,
            'city': job.city,
            'description': job.job_description,
            'pay': job.pay,
            'per': job.per,
            'job_type': job.job_type,
            'date_posted': job.date_posted,
            'users_applied': users
        }
        job_list.append(_job)
        
    return JsonResponse({'jobs': job_list})

def api_view_resume(request, id, job_id):
    user = User.objects.get(id=id)
    job = Job_Post.objects.get(id=job_id)
    
    application_viewed = True
    
    application = Job_Application.objects.get(job=job, applicant=user)
    if application.status == 'NotViewed':
        application.status = 'Viewed'
        application.save()
        application_viewed = False
        
    image_path = user.resume_image

    return JsonResponse ({
        'resume_path': image_path,
        'application_viewed': application_viewed,
        'application_status': application.status if application.status != 'Viewed' else 'select'
    })

def api_group_name(request):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=10))
    
    return JsonResponse({
        'group_name': random_string
    })

def api_conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data_group_name = data['group_name']
        data_id = data['id']
        job_id = data['job_id']
        
        job = Job_Post.objects.get(id=job_id)
        current_user = User.objects.get(id=request.session['user_id'])
        chatmate = User.objects.get(id=data_id)
        
        conversation = Conversation(group_name=data_group_name, job=job)
        conversation.save()
        
        for user in [current_user, chatmate]:
            conversation.people.add(user)
            conversation.save()
        
        return JsonResponse({
            'message': 'Conversation Created Successfully'
        })

def api_retrieve_conversation_id(request, id, job_id):
    try:
        current_user = User.objects.get(id=request.session['user_id'])
        chatmate = User.objects.get(id=id)
        job = Job_Post.objects.get(id=job_id)
        conversations = Conversation.objects.filter(job=job)
    except (Conversation.DoesNotExist, Job_Post.DoesNotExist):
        return JsonResponse({
            'message': 'Failed'
        }) 

    conversation_exist = False
    group_name = ''

    for _conversation in conversations.all():
        if current_user in _conversation.people.all() and chatmate in _conversation.people.all():
            conversation_exist = True
            group_name = _conversation.group_name
        
        
    if conversation_exist:
        return JsonResponse({
            'message': 'Success',
            'group_name': group_name
        })
    else:
        return JsonResponse({
            'message': 'Failed'
        })

def api_set_status(request, user_id, job_id, status):
    applicant = User.objects.get(id=user_id)
    job = Job_Post.objects.get(id=job_id)
    application = Job_Application.objects.get(applicant=applicant, job=job)
    application.status_viewed = False
    application.status = status
    application.save()
    
    return JsonResponse({
        'message': 'Success'
    })