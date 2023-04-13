from django.shortcuts import render
from .models import Form5500
import pandas as pd

# Create your views here.
def charts(request):
    return render(request,'form5500/charts.html')

def state(request):
    state_list = Form5500.objects.order_by('EIN')[:51]
    return render(request,'form5500/state.html', {'state_list': state_list})

def asset(request):
    asset_list = Form5500.objects.order_by('EIN')[:51]
    return render(request,'form5500/asset.html', {'asset_list': asset_list})

def industry(request):
    industry_list = Form5500.objects.order_by('EIN')[:51]
    return render(request,'form5500/industry.html',{'industry_list': industry_list})

#def chart_view(request):
#   qs = Form5500.objects.all()[:10]
#   data = pd.DataFrame(qs)

# def get_queryset(self, request): # new
#         query = self.request.GET.get("q")
#         state_list = Form5500.objects.filter(Sponsor_State__contains = query)
#         return render(request,'form5500/state.html', {'state_list': state_list})