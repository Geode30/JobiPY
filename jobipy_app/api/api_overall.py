from ..models import User, Conversation
from django.http import JsonResponse

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

def api_notification(request):
    current_user = User.objects.get(id=request.session['user_id'])
    conversations = Conversation.objects.filter(people=current_user)
    
    conversations_with_unread_messages = conversations.filter(messages__is_read=False, messages__receiver=current_user).distinct()

    print(conversations_with_unread_messages)
    return JsonResponse({
        'message': 'Success',
        'message_notification': conversations_with_unread_messages.count()
    })

def display_resume_img(id):
    user = User.objects.get(id=id)
    image_path = user.resume_image

    return image_path