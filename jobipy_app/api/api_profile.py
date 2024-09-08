from ..models import User
from django.http import JsonResponse

from pdf2jpg import pdf2jpg
import os

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