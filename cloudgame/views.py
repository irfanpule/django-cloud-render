from django.shortcuts import render


def index(request):
    context = {
        'title': 'Beranda'
    }
    return render(request, 'index.html', context)
