import json
from django.http import JsonResponse
from ..models import User, Preferences
from pdf2jpg import pdf2jpg
import os

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