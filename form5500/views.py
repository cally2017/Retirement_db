from django.shortcuts import render
from django.http import HttpResponse
import csv
import datetime
from .models import Form5500
import pandas as pd
from .utils import get_plot
from django.db.models import Q
import folium

# Create your views here.
def charts(request):
    qs = Form5500.objects.all().values()
    data = pd.DataFrame(qs) 
    print(data['EIN'][:10])
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

def map(request):
    qs = Form5500.objects.all().values()
    data = pd.DataFrame(qs) 
    gb_state_sum = data.groupby("Sponsor_State", as_index =False)["Plan_Asset"].sum()
    lt = [['AL',32.6010112,-86.6807365],['AK',61.3025006,-158.7750198],['AZ',34.1682185,-111.930907],['AR',34.7519275,-92.1313784],['CA',37.2718745,-119.2704153],
          ['CO',38.9979339,-105.550567],['CT',41.5187835,-72.757507],['DE',39.145251,-75.4189206],['DC',38.8993487,-77.0145666],['FL',27.9757279,-83.0229757],
          ['GA',32.6781248,-83.2229757],['HI',20.46,-157.505],['ID',45.4945756,-114.1424303],['IL',39.739318,-89.504139],['IN',39.7662195,-86.441277],
          ['IA',41.9383166,-93.389798],['KS',38.4987789,-98.3200779],['KY',37.8222935,-85.7682399],['LA',30.9733766,-91.4299097],['ME',45.2185133,-69.0148656],
          ['MD',38.8063524,-77.2684162],['MA',42.0629398,-71.718067],['MI',44.9435598,-86.4158049],['MN',46.4418595,-93.3655146],['MS',32.5851062,-89.8772196],
          ['MO',38.3046615,-92.437099],['MT',46.6797995,-110.044783],['NE',41.5008195,-99.680902],['NV',38.502032,-117.0230604],['NH',44.0012306,-71.5799231],
          ['NJ',40.1430058,-74.7311156],['NM',34.1662325,-106.0260685],['NY',40.7056258,-73.97968],['NC',35.2145629,-79.8912675],['ND',47.4678819,-100.3022655],
          ['OH',40.1903624,-82.6692525],['OK',35.3097654,-98.7165585],['OR',44.1419049,-120.5380993],['PA',40.9945928,-77.6046984],['RI',41.5827282,-71.5064508],
          ['SC',33.62505,-80.9470381],['SD',44.2126995,-100.2471641],['TN',35.830521,-85.9785989],['TX',31.1693363,-100.0768425],['UT',39.4997605,-111.547028],
          ['VT',43.8717545,-72.4477828],['VA',38.0033855,-79.4587861],['WA',38.8993487,-77.0145665],['WV',38.9201705,-80.1816905],['WI',44.7862968,-89.8267049],
          ['WY',43.000325,-107.5545669],
        ]
    location = pd.DataFrame(lt,columns=['Sponsor_State','Latitude','Longitude'])
    result = pd.merge(gb_state_sum,location,how='inner', on="Sponsor_State")
    m = folium.Map(location=[37.09024,-95.712891], zoom_start=5, width="%100",height="%100")
    for i in range(len(result["Sponsor_State"])):
        lat = result["Latitude"][i]
        long = result["Longitude"][i]
        r = result["Plan_Asset"][i]/50000000000
        folium.CircleMarker(location = [lat,long], radius=r, fill_color='blue').add_to(m)
    m = m._repr_html_()
    context = {
        'm': m, 
    }  
    return render(request, 'form5500/map.html', context)

def search_state(request): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        state_list = Form5500.objects.order_by('EIN')[:51]
        q = ""
        states = ""
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
                query1 = Q(Q(Sponsor_State__icontains=states))
                query2 = Q(Q(Sponsor_Name__icontains=q))
                state_list = Form5500.objects.filter(query1, query2).values()
        
        context = { 'state_list': state_list,
                    'phrase': states+'-'+q,}

        return render(request, 'form5500/state.html', context) 

def search_industry(request): # new
        #function grabs both drop down menu and search bar input 
        # - if drop down is 'Industry', and 'q' is input - executes query on 'q'
        # - if q is empty, but drop down is not 'Industry' - executes query on drop down
        # - if both q is empty and drop down is 'Industry' - no query executed
        # - else - performs query on both values

        industry_list = Form5500.objects.order_by('EIN')[:51]
        q = ""
        industries = ""
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
                query1 = Q(Q(Industry_Description__icontains=industries))
                query2 = Q(Q(Sponsor_Name__icontains=q))
                industry_list = Form5500.objects.filter(query1, query2).values()
        #Default Output
        else:
             industry_list = Form5500.objects.order_by('EIN')[:51]

        context = {'industry_list': industry_list,
                   'phrase': industries+'-'+q,}
        return render(request, 'form5500/industry.html', context)

def search_asset(request): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        asset_list = Form5500.objects.order_by('EIN')[:51]
        q = ""
        operators = ""
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
        
        context = {'asset_list': asset_list,
                   'phrase': operators+'-'+q,}
        return render(request, 'form5500/asset.html', context)

def state_export(request, q): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        data = Form5500.objects.order_by('EIN')[:51]        
        text = q.split('-')
        #Check if within GET
        if text[0]=='State' and text[1]!='':
        #state drop down is empty
            query = Q(Q(Sponsor_Name__icontains=text[1]))
            data = Form5500.objects.filter(query).order_by('EIN')
        elif text[0]!='State' and text[1]=='':
            # q is empty
            query = Q(Q(Sponsor_State__icontains=text[0]))
            data = Form5500.objects.filter(query).order_by('EIN')            
        elif text[0]!='State' and text[1]!='':
            #Dual query
            query1 = Q(Q(Sponsor_State__icontains=text[0]))
            query2 = Q(Q(Sponsor_Name__icontains=text[1]))
            data = Form5500.objects.filter(query1,query2).order_by('EIN')   
        #Default Output
        else:
            data = Form5500.objects.order_by('EIN')[:51]
        # Export
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=retiment_info' + str(datetime.datetime.now())+'.csv'
        writer = csv.writer(response)
        writer.writerow(['EIN','Sponsor Name','Sponsor Street','Sponsor City','Sponsor State','Sponsor Zipcode','Industry','Broker','Provider','Participant','Asset'])
        for state in data:
            writer.writerow([state.EIN,state.Sponsor_Name,state.Sponsor_Street,state.Sponsor_City,state.Sponsor_State,state.Sponsor_Zipcode,state.Industry_Description,state.Broker_Name,state.Provider_Name,state.Participants,state.Plan_Asset])
        return response

def industry_export(request, q): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        data = Form5500.objects.order_by('EIN')[:51]        
        text = q.split('-')
        #Check if within GET
        if text[0]=='Industry' and text[1]!='':
        #state drop down is empty
            query = Q(Q(Sponsor_Name__icontains=text[1]))
            data = Form5500.objects.filter(query).order_by('EIN')
        elif text[0]!='Industry' and text[1]=='':
            # q is empty
            query = Q(Q(Industry_Description__icontains=text[0]))
            data = Form5500.objects.filter(query).order_by('EIN')            
        elif text[0]!='Industry' and text[1]!='':
            #Dual query
            query1 = Q(Q(Industry_Description__icontains=text[0]))
            query2 = Q(Q(Sponsor_Name__icontains=text[1]))
            data = Form5500.objects.filter(query1,query2).order_by('EIN')   
        #Default Output
        else:
            data = Form5500.objects.order_by('EIN')[:51]
        # Export
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=retiment_info' + str(datetime.datetime.now())+'.csv'
        writer = csv.writer(response)
        writer.writerow(['EIN','Sponsor Name','Sponsor Street','Sponsor City','Sponsor State','Sponsor Zipcode','Industry','Broker','Provider','Participant','Asset'])
        for industry in data:
            writer.writerow([industry.EIN,industry.Sponsor_Name,industry.Sponsor_Street,industry.Sponsor_City,industry.Sponsor_State,industry.Sponsor_Zipcode,industry.Industry_Description,industry.Broker_Name,industry.Provider_Name,industry.Participants,industry.Plan_Asset])
        return response

def asset_export(request, q): # new
        #function will look at search bar first and see if it is specified.
        #then will look at drop down menu 
        # - if drop down is 'State', breaks out.
        # - if query, then it will execute

        data = Form5500.objects.order_by('EIN')[:51]        
        text = q.split('-')
        #Check if within GET
        if text[0]=='Operator' and text[1]!='':
            #operator drop down is empty
            query = Q(Q(Plan_Asset__icontains=q))
            data = Form5500.objects.filter(query).order_by('EIN')
        elif text[0]!='Operator' and text[1]=='':
            # q is empty
            data = Form5500.objects.order_by('EIN')[:51]            
        elif text[0]!='Operator' and text[1]!='':
            #Dual query
            if text[0] == ">": 
                #Dual query
                data = Form5500.objects.filter(Plan_Asset__gt=text[1]).order_by('EIN')
            elif text[0] == ">=": 
                #Dual query
                data = Form5500.objects.filter(Plan_Asset__gte=text[1]).order_by('EIN')
            elif text[0] == "=": 
                #Dual query
                data = Form5500.objects.filter(Plan_Asset__exact=text[1]).order_by('EIN')
            elif text[0] == "<": 
                #Dual query
                data = Form5500.objects.filter(Plan_Asset__lt=text[1]).order_by('EIN')
            elif text[0] == "<=": 
                #Dual query
                data = Form5500.objects.filter(Plan_Asset__lte=text[1]).order_by('EIN')
        #Default Output
        else:
            data = Form5500.objects.order_by('EIN')[:51]
        # Export
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=retiment_info' + str(datetime.datetime.now())+'.csv'
        writer = csv.writer(response)
        writer.writerow(['EIN','Sponsor Name','Sponsor Street','Sponsor City','Sponsor State','Sponsor Zipcode','Industry','Broker','Provider','Participant','Asset'])
        for asset in data:
            writer.writerow([asset.EIN,asset.Sponsor_Name,asset.Sponsor_Street,asset.Sponsor_City,asset.Sponsor_State,asset.Sponsor_Zipcode,asset.Industry_Description,asset.Broker_Name,asset.Provider_Name,asset.Participants,asset.Plan_Asset])
        return response
