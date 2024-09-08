import re
from django.http import JsonResponse
from ..models import User, Preferences

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