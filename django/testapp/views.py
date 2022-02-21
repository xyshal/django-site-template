from django.shortcuts import render
from .models import TestModel

def index(request):
    num_records = TestModel.objects.all().count()
    
    context = { 'num_records' : num_records }

    return render(request, 'index.html', context=context)

