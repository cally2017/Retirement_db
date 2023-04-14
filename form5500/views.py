from django.shortcuts import render
from .models import Form5500
import pandas as pd
from .utils import get_plot
from django.db.models import Count

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

def state(request):
    return render(request,'form5500/state.html')

def asset(request):
    return render(request,'form5500/asset.html')

def industry(request):
    return render(request,'form5500/industry.html')


#def chart_view(request):
#   qs = Form5500.objects.all()[:10]
#   data = pd.DataFrame(qs)