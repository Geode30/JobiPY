from ..models import User, Conversation, Message
from django.http import JsonResponse
import json
import datetime

def api_message(request):
    data = json.loads(request.body)
    conversation_id = data['conversation_id']
    message = data['message']
    current_user = User.objects.get(id=request.session['user_id'])
    chatmate = {}
    conversation = Conversation.objects.get(id=conversation_id)
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%B %d, %Y, %I:%M:%S %p")
    
    for user in conversation.people.all():
        if user != current_user:
            chatmate = user
    
    message = Message(sender=current_user, receiver=chatmate, message=message, is_read=False, date=formatted_date)
    message.save()
    conversation.messages.add(message)
    conversation.save()
    
    return JsonResponse({
        'message': 'Message created. Saved to the conversation'
    })
    
def api_read(request):
    user = User.objects.get(id=request.session['user_id'])
    data = json.loads(request.body)
    conversation_id = data['id']
    conversation = Conversation.objects.get(id=conversation_id)
    
    for message in conversation.messages.filter(is_read=False, receiver=user).order_by('date'):
        _message = Message.objects.get(id=message.id) 
        _message.is_read = True
        _message.save()
            
    return JsonResponse({
        'message': 'Messages Read'
    })

def api_retrieve_conversation_group(request, group_name):
    user = User.objects.get(id=request.session['user_id'])
    chatmate = {}
    messages = []
    try:
        conversation = Conversation.objects.get(group_name=group_name)
        for _user in conversation.people.all():
            if _user != user:
                chatmate = {
                    'id': _user.id,
                    'name': _user.name
                }
        
        for message in conversation.messages.all().order_by('date'):

            sender = {
                'id': message.sender.id,
                'name': message.sender.name
            }
            receiver = {
                'id': message.receiver.id,
                'name': message.receiver.name
            }
            _message = {
                'message': message.message,
                'sender': sender,
                'receiver': receiver,
                'date': message.date
            }
            messages.append(_message)
    except Conversation.DoesNotExist:
        conversation = None  
    
    user = {
        'id': user.id,
        'name': user.name
        }

    if conversation is not None:
        return JsonResponse({
            'message': 'Success',
            'current_user': user,
            'chatmate': chatmate,
            'id': conversation.id,
            'messages': messages
        })
    else:
        return JsonResponse({
            'message': 'Failed'
        })