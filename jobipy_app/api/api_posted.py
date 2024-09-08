from ..models import User, Job_Post, Conversation
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
        for _user in job.users_applied.all():
            __user = {
                'id': _user.id,
                'name': _user.name
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

def api_resume(request, id):
    user = User.objects.get(id=id)
    image_path = user.resume_image

    return JsonResponse ({
        'resume_path': image_path
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
        conversation = Conversation.objects.filter(people__in=[current_user, chatmate], job=job).first()
    except (Conversation.DoesNotExist, Job_Post.DoesNotExist):
        conversation = None  

    if conversation is not None:
        return JsonResponse({
            'message': 'Success',
            'group_name': conversation.group_name
        })
    else:
        return JsonResponse({
            'message': 'Failed'
        })