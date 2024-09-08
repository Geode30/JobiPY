from ..models import User, Preferences, Job_Post
from django.http import JsonResponse
import json

def api_jobs(request):
    user = User.objects.get(id=request.session['user_id'])
    preferences = Preferences.objects.get(user=user)
    jobs = Job_Post.objects.filter(industry=preferences.industry).exclude(poster=user).order_by('-date_posted')
    
    job_list = []
    
    for job in jobs:
        if user not in job.users_applied.all():
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
                'date_posted': job.date_posted
            }
            job_list.append(_job)
        
    return JsonResponse({'jobs': job_list})

def api_search(request, job_title, city=None):
    user = User.objects.get(id=request.session['user_id'])
    
    if (city is not None):
        job_post = Job_Post.objects.filter(job_title=job_title, city=city).exclude(poster=user)
    else:
        job_post = Job_Post.objects.filter(job_title=job_title).exclude(poster=user)
    
    job_list = []
    
    for job in job_post:
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
            'date_posted': job.date_posted
        }
        job_list.append(_job)    
    return JsonResponse({'jobs': job_list})

def api_apply(request):
    data = json.loads(request.body)
    id = data['id']
    
    user = User.objects.get(id=request.session['user_id'])
    
    job = Job_Post.objects.get(id=id)
    job.users_applied.add(user)
    job.save()
    
    return JsonResponse({
        'message': 'Application Submitted Succesfully'
    })