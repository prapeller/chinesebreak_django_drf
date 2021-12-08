from django.shortcuts import render

def index(request):
    context = {
        'title': 'Main',
    }
    return render(request, 'admin_panel/index.html', context)