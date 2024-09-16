from ..models import User, Preferences, Job_Post, Job_Application
from django.http import JsonResponse
import json

def api_index_search(request):
    industry = request.GET['industry']
    job_title = request.GET['job_title']
    city = request.GET['city']
    
    jobs = Job_Post.objects.filter(industry=industry)

    if job_title is not None and job_title != '':
        jobs = jobs.filter(job_title=job_title)
    if city is not None and city != '':
        jobs = jobs.filter(city=city)
    
    jobs_list = []
    
    for job in jobs:
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
            'job_type': job.job_type,
            'date_posted': job.date_posted,
        }
        
        jobs_list.append(job_details)
    
    return JsonResponse({
        'message': 'Success',
        'jobs': jobs_list
    })