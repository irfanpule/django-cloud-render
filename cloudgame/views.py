from django.shortcuts import render


def index(request):
    context = {
        'title': 'Beranda',
        'hide_navbar': True
    }
    return render(request, 'index.html', context)
