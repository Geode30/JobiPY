from ..models import User, Preferences, Job_Post, Job_Application
from django.http import JsonResponse
import json

import datetime

def api_jobs(request):
    user = User.objects.get(id=request.session['user_id'])
    preferences = Preferences.objects.get(user=user)
    jobs = Job_Post.objects.filter(industry=preferences.industry).exclude(poster=user).order_by('-date_posted')
    
    job_list = []
    
    for job in jobs:
        job_type = []
        
        pay_color = '#0CB83C'
        if int(job.pay) < int(preferences.minimum_base_pay):
            pay_color = '#dc3545'
        
        try:
            pref_job_types = preferences.job_type.split(',')
        except AttributeError:
            pref_job_types = preferences.job_type
            
        for _job_type in pref_job_types:
            if _job_type in job.job_type.split(','):
                job_type.append(_job_type)
        
        job_type_set = set(job_type)
        job_type_sep_comma = ','.join(job_type_set)
        
        job_details = {
            'id': job.id,
            'poster': job.poster.name,
            'job_title': job.job_title,
            'company': job.company,
            'city': job.city,
            'description': job.job_description,
            'currency': job.currency,
            'pay': job.pay,
            'per': job.per,
            'job_type': job_type_sep_comma if len(job_type_set) > 0 else job.job_type,
            'date_posted': job.date_posted,
            'pay_color': pay_color,
            'job_type_color': '#0CB83C' if len(job_type_set) > 0 else '#dc3545'
        }

        application = Job_Application.objects.filter(job=job, applicant=user).distinct().first()
        if not application:
            job_list.append(job_details)

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
        application = Job_Application.objects.filter(job=job, applicant=user).distinct().first()
        if not application:
            job_list.append(_job)    

    return JsonResponse({'jobs': job_list})

def api_apply(request):
    data = json.loads(request.body)
    job_id = data['id']

    user = User.objects.get(id=request.session['user_id'])
    job = Job_Post.objects.get(id=job_id)
    
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%B %d, %Y, %I:%M:%S %p")
    
    job_application = Job_Application(job=job, applicant=user, date_applied=formatted_date)
    job_application.save()
    
    return JsonResponse({
        'message': 'Application Submitted Succesfully'
    })