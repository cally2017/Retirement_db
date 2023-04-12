from django.shortcuts import render
from .models import Form5500
import pandas as pd

# Create your views here.
def charts(request):
    return render(request,'form5500/charts.html')

def state(request):
    return render(request,'form5500/state.html')

def asset(request):
    return render(request,'form5500/asset.html')

def industry(request):
    return render(request,'form5500/industry.html')


#def chart_view(request):
#   qs = Form5500.objects.all()[:10]
#   data = pd.DataFrame(qs)