import json
from django.contrib.sessions.backends.cached_db import SessionStore
from django.views import View
from django.shortcuts import render, redirect
from .models import getAPIdata, checkExceedLv, calcMain

# Create your views here.
def gotoCalculate(request):
    return render(request, "input_name.html")

def calcPage(request):
    if request.method == "POST":
        # Input page에서 가져온 캐릭터이름으로 API
        data = getAPIdata(request.POST.get('charName'))
        raid = request.POST.get('raidName')

        prof = {'name': data['ArmoryProfile']['CharacterName'],
        'img': data['ArmoryProfile']['CharacterImage'],
        'avglv' : data['ArmoryProfile']['ItemAvgLevel'],
        'maxlv' : float(data['ArmoryProfile']['ItemMaxLevel'].replace(',',''))
        }
        eqmt = []
        for idx in range(0,6):
            eqmt.append({'Grade': data['ArmoryEquipment'][idx]['Grade'],
                        'Name': data['ArmoryEquipment'][idx]['Name'],
                        'Icon': data['ArmoryEquipment'][idx]['Icon'],
                        'Tooltip': json.loads(data['ArmoryEquipment'][idx]['Tooltip'])
                })
            if idx > 0:
                eqmt[idx]['exceed'] = checkExceedLv(eqmt[idx])
        
        request.session['prof'] = prof
        request.session['eqmt'] = eqmt
        request.session['raid'] = raid  
        return redirect('/calc')
    else:
        prof = request.session['prof']
        eqmt = request.session['eqmt']
        raid = request.session['raid']
        if request.COOKIES.get('opts') is not None:
            opts = json.loads(request.COOKIES.get('opts'))
            opts['hands'] = int(opts['hands'])
            opts['inven'] = int(opts['inven'])
        else:
            opts = None
        context = {
            'prof' : prof,
            'eqmt' : eqmt,
            'raid' : raid,
            'opts' : opts,
        }
        result = calcMain(prof, eqmt, raid, opts)
        context['result'] = result
        context['materialImg'] = "https://i.imgur.com/LrRIH8K.png" if raid=='0' else "https://i.imgur.com/g0URllR.png" if raid=='1' else ''
        print(context['opts'])
    return render(request, "Calculator.html", context)

def error400(request, exception):
    return render(request, 'error.html', status=400)

def error404(request, exception):
    return render(request, 'error.html', status=404)

def error500(request):
    return render(request, 'error.html', status=500)

