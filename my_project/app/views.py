from django.shortcuts import render

def index(request, group_name):
    # Pass the group_name to the template context
    context = {
        'group_name': group_name
    }
    return render(request, 'app/index.html', context)
