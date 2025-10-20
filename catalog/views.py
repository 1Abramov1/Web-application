from django.shortcuts import render

def home(request):
    """Домашняя страница каталога"""
    return render(request, 'catalog/home.html')

def contacts(request):
    """Страница с контактной информацией"""
    return render(request, 'catalog/contacts.html')
