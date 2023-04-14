from django.shortcuts import render
from django.db.models import Q
from .models import Form5500
import pandas as pd

# Create your views here.
def charts(request):
    return render(request,'form5500/charts.html')

def search_state(request): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        # Only search bar specified
        if 'q' in request.GET:
            q = request.GET['q']
            if q:
                query = Q(Q(Sponsor_State__icontains=q))
                state_list = Form5500.objects.filter(query).order_by('EIN')
            else:
                state_list = Form5500.objects.order_by('EIN')[:51]
        else:
            state_list = Form5500.objects.order_by('EIN')[:51]

        # Only drop down specified
        if 'states' in request.GET:
            states = request.GET['states']
            if states == 'State':
                next
            elif states:
                query = Q(Q(Sponsor_State__icontains=states))
                state_list = Form5500.objects.filter(query).order_by('EIN')
            else:
                state_list = Form5500.objects.order_by('EIN')[:51]
        else:
            state_list = Form5500.objects.order_by('EIN')[:51]
        
        context = {
            'state_list': state_list
        }
        return render(request, 'form5500/state.html', context)

def search_asset(request): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        # Only search bar specified
        if 'q' in request.GET:
            q = request.GET['q']
            if q:
                query = Q(Q(Plan_Asset__icontains=q))
                asset_list = Form5500.objects.filter(query).order_by('EIN')
            else:
                asset_list = Form5500.objects.order_by('EIN')[:51]
        else:
            asset_list = Form5500.objects.order_by('EIN')[:51]

        # Only drop down specified
        if 'operator' in request.GET:
            operators = request.GET['operator']
            if operators == 'Operator':
                next
            elif operators:
                query = Q(Q(Plan_Asset__icontains=operators))
                asset_list = Form5500.objects.filter(query).order_by('EIN')
            else:
                asset_list = Form5500.objects.order_by('EIN')[:51]
        else:
            asset_list = Form5500.objects.order_by('EIN')[:51]
        
        context = {
            'asset_list': asset_list
        }
        return render(request, 'form5500/asset.html', context)

def search_industry(request): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        # Only search bar specified
        if 'q' in request.GET:
            q = request.GET['q']
            if q:
                query = Q(Q(Industry_Description__icontains=q))
                industry_list = Form5500.objects.filter(query).order_by('EIN')
            else:
                industry_list = Form5500.objects.order_by('EIN')[:51]
        else:
            industry_list = Form5500.objects.order_by('EIN')[:51]

        # Only drop down specified
        if 'industries' in request.GET:
            industries = request.GET['industries']
            if industries == 'Industry':
                next
            elif industries:
                query = Q(Q(Industry_Description__icontains=industries))
                industry_list = Form5500.objects.filter(query).order_by('EIN')
            else:
                industry_list = Form5500.objects.order_by('EIN')[:51]
        else:
            industry_list = Form5500.objects.order_by('EIN')[:51]
        
        context = {
            'industry_list': industry_list
        }
        return render(request, 'form5500/industry.html', context)


# def state(request):
#     state_list = Form5500.objects.order_by('EIN')[:51]
#     return render(request,'form5500/state.html', {'state_list': state_list})

# def asset(request):
#     asset_list = Form5500.objects.order_by('EIN')[:51]
#     return render(request,'form5500/asset.html', {'asset_list': asset_list})

# def industry(request):
#     industry_list = Form5500.objects.order_by('EIN')[:51]
#     return render(request,'form5500/industry.html',{'industry_list': industry_list})