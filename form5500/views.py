from django.shortcuts import render
from .models import Form5500
import pandas as pd
from .utils import get_plot
from django.db.models import Count
from django.db.models import Q

# Create your views here.
def charts(request):
    qs = Form5500.objects.all().values()
    data = pd.DataFrame(qs) 
    gb_state_cnt = data.groupby("Sponsor_State", as_index =False).count().nlargest(10,"EIN")
    gb_state_cnt = gb_state_cnt.sort_values(by=['EIN'])
    gb_state_sum = data.groupby("Sponsor_State", as_index =False)["Plan_Asset"].sum().nlargest(10,"Plan_Asset")
    gb_state_sum = gb_state_sum.sort_values(by=['Plan_Asset'])
    gb_industry_sum = data.groupby("Industry_Description", as_index =False)["Plan_Asset"].sum()
    gb_industry_sum = gb_industry_sum.sort_values(by=['Plan_Asset'], ascending=False)
    #print(gb_state_cnt)
    chart = get_plot(gb_state_cnt["Sponsor_State"],gb_state_cnt["EIN"],gb_state_sum["Sponsor_State"],gb_state_sum["Plan_Asset"],
                     gb_industry_sum["Industry_Description"],gb_industry_sum["Plan_Asset"])
    return render(request,'form5500/charts.html',{'chart':chart})

def search_state(request): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        # Only search bar specified
        if 'q' in request.GET:
            q = request.GET['q']
            if q:
                query = Q(Q(Sponsor_Name__icontains=q))
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


#def chart_view(request):
#   qs = Form5500.objects.all()[:10]
#   data = pd.DataFrame(qs)