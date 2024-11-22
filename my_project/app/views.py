from django.shortcuts import render
from . models import Chat, Group

def index(request, group_name):
    # Pass the group_name to the template context

    group = Group.objects.filter(name = group_name).first()
    chat = []
    
    if group:
        chat = Chat.objects.filter(group=group)
    else:    
        group = Group(name=group_name)
        group.save()

    context = {
        'group_name': group_name,
        'chat':chat
    }
    return render(request, 'app/index.html', context)
