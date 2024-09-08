import json
import re
from django.http import JsonResponse
from ..models import User

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