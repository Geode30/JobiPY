from .models import User, Preferences, Job_Post
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import datetime

from pdf2jpg import pdf2jpg
import os

def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data["firstname"]
        last_name = data['lastname']
        name = f'{first_name} {last_name}'
        email = data['email']
        password = data['password']
        confirm_pass = data['confirmPass']
        
        try:
            checkUser = User.objects.get(email=email)
        except User.DoesNotExist:
            checkUser = None

        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if re.match(email_pattern, email) is None:
            return JsonResponse({
                'message' : 'Invalid Email'
            })
        elif password != confirm_pass:
            return JsonResponse({
                'message' : 'Password does not match'
            })
        elif checkUser is not None:
            return JsonResponse({
                'message' : 'This email is associated with an existing user'
            })
        else:
            user = User(name=name, email=email, password=password)
            user.set_password(password)
            user.save()
            return JsonResponse({
                'message' : 'User Created Successfully'
            })
    else:
        return JsonResponse({
            'message': 'Make a POST request'
        })
            
def api_login(request, email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None
    
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_pattern, email) is None:
        return JsonResponse({
            'message' : 'Invalid email'
        }) 
    elif user is None:
        return JsonResponse({
            'message' : 'Email is not registered'
        })  
    elif user.check_password(password) is None:
        return JsonResponse({
            'message': 'Wrong password'
        })
    else:
        if 'user_id' not in request.session:
            request.session['user_id'] = 0
        request.session['user_id'] = user.id
        try:
            preferences = Preferences.objects.get(user=user)
        except Preferences.DoesNotExist:
            preferences = None
        if preferences is None:
            preferences = False
        else:
            preferences = True
            
        return JsonResponse({
            'message': 'Login Successful',
            'preferences': preferences,
            'id': user.id,
            'name': user.name,
            'email': user.email
        })

def api_setup(request):    
    if request.method == 'POST':
        industry = request.POST['industry']
        minimum_base_pay = request.POST['minimum_base_pay']
        per = request.POST['per']
        job_type = request.POST['job_type']
        
        contact_number = request.POST['contact_number']
        city = request.POST['city']
        resume = request.FILES['resume']
        
        if not industry or not minimum_base_pay or not per or not job_type or not contact_number or not city or not resume:
            return JsonResponse({
                'message': 'Please fill all the required fields'
            })
        else:           
            user = User.objects.get(id=request.session['user_id'])
            user.contact_number = contact_number
            user.resume = resume
            user.city = city
            user.save()
            
            pdf_path = user.resume.path
            output_path = 'media/output'
            
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                
            convert_pdf_to_jpg = pdf2jpg.convert_pdf2jpg(pdf_path, output_path, pages="ALL")
            user.resume_image = convert_pdf_to_jpg[0]['output_jpgfiles'][0]
            user.save()
            
            preferences = Preferences(user=user, industry=industry, minimum_base_pay=minimum_base_pay, per=per, job_type=job_type)
            preferences.save()
            
            return JsonResponse({
                'message': 'Preferences Created Successfully'
            })
    elif request.method == 'PUT':
        data = json.loads(request.body)
        industry = data['industry']
        minimum_base_pay = data['minimum_base_pay']
        per = data['per']
        job_type = data['job_type']
        
        contact_number = data['contact_number']
        city = data['city']
        
        if not industry or not minimum_base_pay or not per or not job_type or not contact_number or not city:
            return JsonResponse({
                'message': 'Please fill all the required fields'
            })
        else:           
            user = User.objects.get(id=request.session['user_id'])
            preferences = Preferences.objects.get(user=user)
            
            preferences.industry = industry
            preferences.minimum_base_pay = minimum_base_pay
            preferences.per = per
            preferences.job_type = job_type
            
            user.contact_number = contact_number
            user.city = city
            
            preferences.save()
            user.save()
            
            return JsonResponse({
                'message': 'Preferences Updated Successfully'
            })

    else:
        return JsonResponse({
            'message': 'Make a POST or PUT request'
        })
        
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
        return JsonResponse({
            'message': 'Logout Successfully',
        })   
        
def api_jobs(request):
    user = User.objects.get(id=request.session['user_id'])
    preferences = Preferences.objects.get(user=user)
    jobs = Job_Post.objects.filter(industry=preferences.industry).exclude(poster=user).order_by('-date_posted')
    
    job_list = []
    
    for job in jobs:
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

def api_get_preferences(request):
    user = User.objects.get(id=request.session['user_id'])
    try:
        preferences = Preferences.objects.get(user=user)
    except Preferences.DoesNotExist:
        preferences = None
        
    if preferences is not None:
        return JsonResponse({
            'response': 'Successful',
            'id': preferences.id,
            'user': preferences.user.name,
            'industry': preferences.industry,
            'minimum_base_pay':preferences.minimum_base_pay,
            'per':preferences.per,
            'job_type':preferences.job_type,
            'email': preferences.user.email,
            'contact_number': preferences.user.contact_number,
            'city': preferences.user.city,
            'resume': preferences.user.resume.path
        })
    else:
        return JsonResponse({
            'response': 'Failed',
        })
        
        
def api_replace_resume(request):
    user = User.objects.get(id=request.session['user_id'])
    
    resume = request.FILES['resume']
    user.resume = resume
    user.save()
    
    pdf_path = user.resume.path
    output_path = 'media/output'
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    convert_pdf_to_jpg = pdf2jpg.convert_pdf2jpg(pdf_path, output_path, pages="ALL")
    user.resume_image = convert_pdf_to_jpg[0]['output_jpgfiles'][0]
    user.save()
    
    return JsonResponse({
        'message': 'Resume Replaced Successfully'
    })

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

def api_posted(request):
    user = User.objects.get(id=request.session['user_id'])
    posted_jobs = Job_Post.objects.filter(poster=user).order_by('-date_posted')
    
    job_list = []
    
    
    for job in posted_jobs:
        users = []
        for _user in job.users_applied.all():
            users.append(_user.name)
        
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
        print(users)
        job_list.append(_job)
        
    return JsonResponse({'jobs': job_list})

def api_resume(request, name):
    user = User.objects.get(name=name)
    image_path = user.resume_image

    return JsonResponse ({
        'resume_path': image_path
    })

def display_resume_img(id):
    user = User.objects.get(id=id)
    image_path = user.resume_image

    return image_path