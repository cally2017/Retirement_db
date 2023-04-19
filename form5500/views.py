from django.shortcuts import render
from .models import Form5500
import pandas as pd
from .utils import get_plot
from django.db.models import Count
from django.db.models import Q, F

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
        #function grabs both drop down menu and search bar input 
        # - if drop down is 'State', and 'q' is input - executes query on 'q'
        # - if q is empty, but drop down is not 'State' - executes query on drop down
        # - if both q is empty and drop down is 'State' - no query executed
        # - else - performs query on both values

        #Check if within GET
        if 'q' and 'states' in request.GET :
            #collect variables
            q = request.GET['q'].upper()
            states = request.GET['states']
            if states == 'State':
                #state drop down is empty
                query = Q(Q(Sponsor_Name__icontains=q))
                state_list = Form5500.objects.filter(query).order_by('EIN')
            elif q=='':
                # q is empty
                query = Q(Q(Sponsor_State__icontains=states))
                state_list = Form5500.objects.filter(query).order_by('EIN')
            elif states=='State' and q=='':
                #No query - Resort to Default view
                state_list = Form5500.objects.order_by('EIN')[:51]
            else: 
                #Dual query
                state_list = Form5500.objects.filter(Sponsor_Name = q, Sponsor_State = states).values()
        #Default Output
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

        #Check if within GET
        if 'q' and 'operator' in request.GET :
            #collect variables
            q = request.GET['q'].upper()
            operators = request.GET['operator']
            if operators == 'Operator':
                #operator drop down is empty
                query = Q(Q(Plan_Asset__icontains=q))
                asset_list = Form5500.objects.filter(query).order_by('EIN')
            elif q=='':
                # q is empty
                asset_list = Form5500.objects.order_by('EIN')[:51]
            elif operators=='Operator' and q=='':
                #No query - Resort to Default view
                asset_list = Form5500.objects.order_by('EIN')[:51]
            elif operators == ">": 
                #Dual query
                asset_list = Form5500.objects.filter(Plan_Asset__gt=q).values()
            elif operators == ">=": 
                #Dual query
                asset_list = Form5500.objects.filter(Plan_Asset__gte=q).values()
            elif operators == "=": 
                #Dual query
                asset_list = Form5500.objects.filter(Plan_Asset__exact=q).values()
            elif operators == "<": 
                #Dual query
                asset_list = Form5500.objects.filter(Plan_Asset__lt=q).values()
            elif operators == "<=": 
                #Dual query
                asset_list = Form5500.objects.filter(Plan_Asset__lte=q).values()
        #Default Output
        else:
                asset_list = Form5500.objects.order_by('EIN')[:51]
        context = {
            'asset_list': asset_list
        }
        return render(request, 'form5500/asset.html', context)

def search_industry(request): # new
        #function grabs both drop down menu and search bar input 
        # - if drop down is 'Industry', and 'q' is input - executes query on 'q'
        # - if q is empty, but drop down is not 'Industry' - executes query on drop down
        # - if both q is empty and drop down is 'Industry' - no query executed
        # - else - performs query on both values

        #Check if within GET
        if 'q' and 'industries' in request.GET :
            #collect variables
            q = request.GET['q'].upper()
            industries = request.GET['industries']
            if industries == 'Industry':
                #industry drop down is empty
                query = Q(Q(Sponsor_Name__icontains=q))
                industry_list = Form5500.objects.filter(query).order_by('EIN')
            elif q=='':
                # q is empty
                query = Q(Q(Industry_Description__icontains=industries))
                industry_list = Form5500.objects.filter(query).order_by('EIN')
            elif industries=='Industry' and q=='':
                #No query - Resort to Default view
                industry_list = Form5500.objects.order_by('EIN')[:51]
            else: 
                #Dual query
                industry_list = Form5500.objects.filter(Sponsor_Name = q, Industry_Description = industries).values()
        #Default Output
        else:
                industry_list = Form5500.objects.order_by('EIN')[:51]
        
        
        context = {
            'industry_list': industry_list
        }
        return render(request, 'form5500/industry.html', context)
