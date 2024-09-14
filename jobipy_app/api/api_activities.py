from ..models import User, Job_Post, Job_Application
from django.http import JsonResponse

from datetime import datetime

def api_applied_jobs(request):
    user = User.objects.get(id=request.session['user_id'])
    jobs = Job_Post.objects.all()
    
    jobs_applied = []
    
    for job in jobs:
        application = Job_Application.objects.filter(job=job, applicant=user).distinct().first()
        if application:
            datetime_format = "%B %d, %Y, %I:%M:%S %p"
            datetime_obj = datetime.strptime(application.date_applied, datetime_format)
            date_str = datetime_obj.strftime("%B %d, %Y")
            _ = {
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
            'date_applied': date_str,
            'status': application.current_status()
            }
            
            jobs_applied.append(_)
    
    return  JsonResponse({
        'message': 'Succesfull',
        'jobs_applied': jobs_applied
    })
    