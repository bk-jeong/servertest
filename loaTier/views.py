import pandas as pd
import json
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tier

# Create your views here.

# 각인 dictionary 초기화
def getEngvInit():
    egv_init = {
        "버서커-비기": 0, "버서커-광기": 0, "디트-분망": 0, "디트-중수": 0, "워로드-고기": 0,
        "워로드-전태": 0, "슬레-처단": 0, "슬레-포식": 0, "배마-오의": 0, "배마-초심": 0,
        "창술-절정": 0, "창술-절제": 0, "인파-체술": 0, "인파-충단": 0, "기공-역천": 0,
        "기공-세멕": 0, "스커-일격": 0, "스커-난무": 0, "브커-수라": 0, "브커-권왕": 0,
        "스카-유산": 0, "스카-기술": 0, "블래-포강": 0, "블래-화강": 0, "호크-두동": 0,
        "호크-죽습": 0, "데헌-강무": 0, "데헌-핸드": 0, "건슬-피메": 0, "건슬-사시": 0,
        "서머너-교감": 0, "서머너-상소": 0, "알카-황제": 0, "알카-황후": 0, "소서-점화": 0,
        "소서-환류": 0, "데모닉-충동": 0, "데모닉-억제": 0, "블레-버스트": 0, "블레-잔재": 0,
        "리퍼-달소": 0, "리퍼-갈증": 0, "소울-만월": 0, "소울-그믐": 0, "기상-질풍": 0,
        "기상-이슬비": 0, "홀나-축오": 0, "홀나-심판": 0, "바드-절구": 0, "바드-용맹": 0,
        "도화가-만개": 0, "도화가-회귀": 0,
        }
    return egv_init
# 티어 dictionary 초기화
def getTierInit():
    res = {"tier1": "", "tier2": "", "tier3": "", "tier4": "", "tier5": "", "tierout": ""}
    return res

def home(request):
    return render(request, "home.html")

def make(request, group):
    try:
        pk = Tier.objects.last().pk
        raid = request.get_full_path().replace('make/','')
        context = {"engvs": getEngvInit(), "raid":raid.replace('/',''), "pk": pk}
        return render(request, "tierMaker.html", context)
    except Exception:
        raid = request.get_full_path().replace('make/','')
        context = {"engvs": getEngvInit(), "raid":raid.replace('/',''), "pk": 0}
        return render(request, "tierMaker.html", context)


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
            id = str(int(id)+1)
            return HttpResponseRedirect("/res/"+group+"/"+id)

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
        return print(str(e))

def statitcs(request):
    try:
        # Tier 테이블에 있는 데이터 가져오기
        rname = request.GET.get('raid')
        
        data = Tier.objects.filter(rname=rname).values()
        
        alldf = pd.DataFrame(data).loc[
            :, ["tier1", "tier2", "tier3", "tier4", "tier5", "tierout"]
        ]
        ndata = len(alldf)
        
        # egv_init이라는 변수를 넣을 상위 dictionary
        return_obj = getTierInit()

        # 평균 티어표를 만들기 위한 각 각인의 점수를 넣을 score(dictionary)
        score = getEngvInit()

        # return_obj의 key(각 티어)에 egv_init(value) 설정
        for i in return_obj.keys():
        # egv_init = 각인명 - 각 티어에 매겨진 횟수
            return_obj[i] = getEngvInit()

        # 각인 count
        for i in range(ndata):     # DB row 수 만큼 반복
            for j in return_obj.keys(): # 각 티어만큼 반복
                for k in score.keys():   # 각인 개수만큼 반복
                    if alldf[j].str.contains(k)[i]:
                        return_obj[j][k] += 1   # 특정 티어의 특정 각인의 value 1씩 더한다
                        if j == "tier1":
                            score[k] += return_obj[j][k] * 5 / ndata
                        elif j == "tier2":
                            score[k] += return_obj[j][k] * 4 / ndata
                        elif j == "tier3":
                            score[k] += return_obj[j][k] * 3 / ndata
                        elif j == "tier4":
                            score[k] += return_obj[j][k] * 2 / ndata
                        elif j == "tier5":
                            score[k] += return_obj[j][k] / ndata
        # 점수를 큰 순서대로 정렬
        sorted_score = sorted(score.items(), key=lambda item: item[1], reverse=True)
        #print(sorted_score)
        
        # html에서 보여줄 티어표
        context = {
            "raid" : rname,
            "tier1": [],
            "tier2": [],
            "tier3": [],
            "tier4": [],
            "tier5": [],
            "tierout": [],
        }
        # 점수를 기반으로 context에 각인명 넣어주기
        for x, y in sorted_score:
            if y >= 4.0:
                context["tier1"] += [x]
            elif y >= 3.0:
                context["tier2"] += [x]
            elif y >= 2.0:
                context["tier3"] += [x]
            elif y >= 1.0:
                context["tier4"] += [x]
            elif y > 0:
                context["tier5"] += [x]
            else:
                context["tierout"] += [x]

        # 통계(비율) 계산하기
        engv_statics = getEngvInit()
        for engv in engv_statics.keys():
            engv_statics[engv] = {"tier1": 0, "tier2": 0, "tier3": 0, "tier4": 0, "tier5": 0, "tierout": 0}
            for tier in return_obj.keys():
                engv_statics[engv][tier] = return_obj[tier][engv] / ndata
        engv_name = list(engv_statics.keys())
        engv_statics = json.dumps(engv_statics)
        return render(request, "allResult.html" ,{'context': context, 'engv_statics':engv_statics, "engv_name":engv_name})
    except Exception as e:
        return print(str(e))
