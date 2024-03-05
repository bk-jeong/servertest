import pandas as pd
import json
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tier
from .utils import StaticResult as sr

# Create your views here.

def home(request):
    return render(request, "home.html")

def make(request, group):
    try:
        if(Tier.objects.last() != None):
            pk = Tier.objects.last().pk
        else:
            pk = 1
        raid = request.get_full_path().replace('make/','')
        context = {"engvs": sr.getEngv(), "raid":raid.replace('/',''), "pk": str(pk)}
        return render(request, "tierMaker.html", context)
    except Exception as e:
        print(str(e))
        return render(request, "error.html")

def personal(request, group, id):
    try:
        if request.method == "POST":
        # Insert ORM
            tier = Tier(
                tier1=request.POST.get("1tia"),
                tier2=request.POST.get("2tia"),
                tier3=request.POST.get("3tia"),
                tier4=request.POST.get("4tia"),
                tier5=request.POST.get("5tia"),
                tierout=request.POST.get("tierout"),
                rname=request.POST.get("raid"),
                )
        # DB save
            tier.save()
            id = Tier.objects.last().pk
            return HttpResponseRedirect("/res/"+group+"/"+str(id))

        # Select ORM (lastest DB row)
        tierRes = Tier.objects.filter(id=int(id))

        # Returon Dictionary Object
        context = {
            "raid": tierRes[0].rname,
            "tier1": tierRes[0].tier1.split(","),
            "tier2": tierRes[0].tier2.split(","),
            "tier3": tierRes[0].tier3.split(","),
            "tier4": tierRes[0].tier4.split(","),
            "tier5": tierRes[0].tier5.split(","),
            "tierout": tierRes[0].tierout.split(","),
        }
        return render(request, "userResult.html", context)
    except Exception as e:
        print(str(e))
        return render(request, "error.html")

def statitcs(request):
    try:
        # Tier 테이블에 있는 데이터 가져오기
        raid = request.GET.get('raid')
        tier = list(sr.tierName.keys())
        if len(Tier.objects.filter(rname=raid)) > 0:
            data = Tier.objects.filter(rname=raid).values()
            alldf = pd.DataFrame(data).loc[:, tier]
            ndata = len(alldf)
            tier_Cnt = sr.tierPerEngv(ndata, alldf)
            engv_Pick = sr.getEngvPick(tier_Cnt)
            engv_Score = sr.getEngvScore(tier_Cnt,engv_Pick)

            tier_Cnt['OP']=tier_Cnt.pop('tier1')
            tier_Cnt['1티어']=tier_Cnt.pop('tier2')
            tier_Cnt['2티어']=tier_Cnt.pop('tier3')
            tier_Cnt['3티어']=tier_Cnt.pop('tier4')
            tier_Cnt['4티어']=tier_Cnt.pop('tier5')
            tier_Cnt['선택없음']=tier_Cnt.pop('tierout')

            engv_statics = sr.getEngvStatics(ndata,tier_Cnt,engv_Pick)
        else:
            ndata = 0
            engv_Score = {'tier1':[],'tier2':[],'tier3':[],'tier4':[],'tier5':[],'tierout':list(sr.engvName.keys())}
            engv_statics = sr.getEngv()
            for en in sr.engvName.keys():
                engv_statics[en] = {'OP': 0, '1티어': 0, '2티어': 0, '3티어': 0, '4티어': 0, '선택없음': 0}

        # html에서 보여줄 티어표
        context = {"raid" : raid,}
        # 점수를 기반으로 context에 각인명 넣어주기
        context.update(engv_Score)
        engv_statics.update({'데이터개수':ndata})
        engv_name = list(sr.engvName.keys())
        engv_statics = json.dumps(engv_statics)
        return render(request, "allResult.html" ,{'context': context, 'engv_statics':engv_statics, "engv_name":engv_name})
    except Exception as e:

        return render(request, "error.html")

def error400(request, exception):
    return render(request, 'error.html', status=400)

def error404(request, exception):
    return render(request, 'error.html', status=404)

def error500(request):
    return render(request, 'error.html', status=500)
