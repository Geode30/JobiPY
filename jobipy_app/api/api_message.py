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
    
    message = Message(sender=current_user, receiver=chatmate, conversation=conversation, message=message, is_read=False, date=formatted_date)
    message.save()
    conversation.updated = formatted_date
    conversation.save()
    
    return JsonResponse({
        'message': 'Message created. Saved to the conversation'
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
                    'name': conversation.job.company if conversation.job.poster.name == _user.name else _user.name,
                }
            
        _messages = Message.objects.filter(conversation=conversation)
        
        for message in _messages.all().order_by('date'):
            sender = {
                'id': message.sender.id,
                'name': message.sender.name,
            }
            receiver = {
                'id': message.receiver.id,
                'name': message.receiver.name
            }
            _ = {
                'message': message.message,
                'sender': sender,
                'receiver': receiver,
                'date': message.date
            }
            messages.append(_)
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
            'company': conversation.job.company,
            'messages': messages
        })
    else:
        return JsonResponse({
            'message': 'Failed'
        })