from ..models import User, Job_Post
from django.http import JsonResponse

import datetime

def api_post(request):
    if request.method == 'POST':
        poster = User.objects.get(id=request.session['user_id'])
        industry = request.POST['industry']
        job_title = request.POST['job_title']
        company = request.POST['company']
        job_description = request.POST['description']
        city = request.POST['city']
        pay = request.POST['minimum_base_pay']
        per = request.POST['per']
        job_type = request.POST['job_type']
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%B %d, %Y, %I:%M %p")
                
        if not industry or not pay or not per or not job_type or not job_title or not city or not company or not job_description:
            return JsonResponse({
                'message': 'Please fill all the required fields'
            })
        else:           
            job_post = Job_Post(poster=poster, industry=industry, job_title=job_title, company=company, job_description=job_description, city=city, pay=pay, per=per, job_type=job_type, date_posted=formatted_date)
            
            job_post.save()
            
            return JsonResponse({
                'message': 'Job Post Successfully Created'
            })
    else:
        return JsonResponse({
            'message': 'Make a POST request'
        })