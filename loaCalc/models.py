from django.db import models

import requests
import math

# Create your models here.

def getAPIdata(charname):
    header = {
        "accept": "application/json",
        "authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDA0ODgzNzkifQ.FaywmL7EyTsWVeUOKs_XINBesuf_aMte5qEM2vU_4IYfV1GmhCZOcNZwVm75OSP96vRtiKpFFsu5_dCrxINpp6wYmo3smv4BbveQcRTyTpI7oxXWRSgpaCUowoVVhiVApVLsKkjq1IK1u5KxualUQyR0pS8Vgm2KAlh9fTa3VadLWQDOj7KrHpDI-cXtDQxu9Fc7do0yhIe4ZT1JQ8hhT2AL3W0khu5CLLFGchP_cVcmdguVurc7hTFv5gBeQI1f2R9xeLAAzL0JIXWtwa5a4DwYiagTJt-m3prplXNNfBhP9kvNtpH_2XcpC-LT4a_o3HZA-680iErjy-3Nqc2kOg",
    }

    # 캐릭터 정보 가져올 URL
    url = f"https://developer-lostark.game.onstove.com/armories/characters/{charname}?filters=profiles%2Bequipment"
    return requests.get(url, headers=header).json()

def calcRequire(eqmt, raid):
    amoEqmt = [d["Name"] for d in eqmt]  # 현재 장착 중인 장비
    trans = [0,0,0,0,0,0]  # 장착 장비의 초월 레벨
    amoCheck = []  # 계승 장비 체크 (계승 필요하면 True, 필요 없으면 False)
    # 계승 확인용 장비명
    valid_amoname = [
        "희생된 지배의 굴레",
        "고요한 광기의 지배",
        "짓눌린 배신의 구속",
        "가라앉은 욕망의 배신",
        "쇠락한 갈망의 그을림",
        "사로잡힌 광기의 갈망",
        "부패한 파괴의 제물",
        "억눌린 마수의 파괴",
        "미약한 매혹의 저주",
        "정화된 욕망의 매혹",
        "유인된 사멸의 종언",
        "타락한 마수의 사멸",
        "왜곡된 악몽의 궤적",
        "전이된 몽환의 악몽",
        "남겨진 환각의 가르침",
        "차오른 몽환의 환각",
        "떠도는 구원의 타륜",
        "도래한 군단의 구원",
    ]
    require = 0  # 필요한 재료 개수
    
    # 필요한 재료 개수 계산하기
    if raid == '0':  
        for idx in range(0, 6):
            amoCheck.append(True)
            if (
                any(str in amoEqmt[idx] for str in valid_amoname)
                or eqmt[idx]["Grade"] == "에스더"
            ):
                amoCheck[idx] = False
            if idx == 0 and amoCheck[idx]:
                require += 100
            elif idx > 0 and amoCheck[idx]:
                require += 40
    elif raid == '1':
        target = 7
        for idx in range(1, 6):
            trans[idx] = eqmt[idx]['exceed']
            if trans[idx] < target:
                if trans[idx] > 2:
                    require += (target - trans[idx]) * 20
                else:
                    require += (3 - trans[idx]) * 15 + (target - 3) * 20
    
    return require

def checkExceedLv(eqmt):
    trans = 0
    for key in eqmt["Tooltip"].keys():
        if "Element_000" in eqmt["Tooltip"][key]["value"]:
            if "topStr" in eqmt["Tooltip"][key]["value"]["Element_000"]:
                if ("초월" in eqmt["Tooltip"][key]["value"]["Element_000"]["topStr"]):
                    trans = int(eqmt["Tooltip"][key]["value"]["Element_000"]["topStr"][56])
                    break
    return trans

def getDefaultOpts(prof, raid, require):
    mxlv = prof["maxlv"]  # 캐릭터 최대 달성 레벨 API data
    freward = False
    auction = False
    hands = 0

    if raid == '0':
        if mxlv < 1600:
            enter = [1, 1, 1, 0]
            if mxlv < 1580:
                freward = True
                hands = 5
        else:
            enter = [3, 3, 3, 0]
        auction = True
    elif raid == '1':
        if mxlv < 1630:
            enter = [1, 1, 1, 0]
            if mxlv < 1610:
                freward = True
        else:
            enter = [3, 3, 3, 0]

    opts = {
        "entries": enter,  # 관문 입장 정보 (0 : X , 1 : 노말_더보기ㅇ, 2 : 노말_더보기x, 3: 하드_더보기ㅇ, 4: 하드_더보기x)
        "auction": auction,  # 경매 참여 여부(일리아칸)
        "fstreward": freward,  # 첫 클리어 보상 여부
        "hands": hands,  # 아크투르스 손길 남은 횟수
        "inven": 0,  # 보유 중인 재료 개수
        "require": require,
    }
    return opts

def getRaidInfo(raid):
    info = {"reward": [], "spend": []}
    if raid == '0':
        info["reward"] = [[3, 7], [3, 7], [5, 8]]
        info["spend"] = [[900, 1200], [1100, 1400], [1500, 1900]]
    elif raid == '1':
        info["reward"] = [[3, 6], [4, 8], [6, 12], [0, 12]]
        info["spend"] = [[1500, 2000], [1800, 2400], [2500, 2800], [0, 3600]]
    return info


def getRewardPWeek(info, opts):
    reward = []
    totalReward = 0
    totalSpend = 0
    for i in range(len(opts["entries"])):
        if opts["entries"][i] != 0:
            reward.append({"reward": 0, "spend": 0})
            if opts["entries"][i] > 2:
                reward[i]["reward"] = (
                    info["reward"][i][1] * 2
                    if opts["entries"][i] % 2 == 1
                    else info["reward"][i][1]
                )
                reward[i]["spend"] = (
                    info["spend"][i][1] if opts["entries"][i] % 2 == 1 else 0
                )
            else:
                reward[i]["reward"] = (
                    info["reward"][i][0] * 2
                    if opts["entries"][i] % 2 == 1
                    else info["reward"][i][0]
                )
                reward[i]["spend"] = (
                    info["spend"][i][0] if opts["entries"][i] % 2 == 1 else 0
                )
            totalReward += reward[i]["reward"]
            totalSpend += reward[i]["spend"]
        else:
            break

    reward.append({"tReward": totalReward, "tSpend": totalSpend})

    return reward


def optimizeGate1(optmz):
    for j in range(optmz["weeks"], 0, -1):
        if (
            optmz["spare"][0] - optmz["gapAdd"][optmz["deployGold"][0][0]] * j
            < optmz["gapAdd"][optmz["deployGold"][0][0]]
        ):
            optmz["spare"][0] = (
                optmz["spare"][0] - optmz["gapAdd"][optmz["deployGold"][0][0]] * j
            )
            optmz["spareAdd"][0] = j
            while optmz["spare"][0] < 0:
                optmz["spareAdd"][0] -= 1
                optmz["spare"][0] += optmz["gapAdd"][optmz["deployGold"][0][0]]
            break
    return optmz


def optimizeGate2(optmz):
    for k in range(0, optmz["weeks"] + 1):
        if optmz["spare"][1] > optmz["gapAdd"][optmz["deployGold"][0][0]]:
            if optmz["spare"][1] - optmz["gapAdd"][optmz["deployGold"][1][0]] > 0:
                optmz["spare"][1] = optmz["spare"][1] - (
                    0 if k == 0 else optmz["gapAdd"][optmz["deployGold"][1][0]]
                )
                optmz["spareAdd"][1] = k
                optmz["spare"][0] = optmz["spare"][1]
                optimizeGate1(optmz)
                optmz["spare"][1] = optmz["spare"][0]
                if optmz["gapAdd"][optmz["deployGold"][1][0]] == 0:
                    optmz["spareAdd"][1] = 0
                    break
            else:
                optmz["spareAdd"][1] = k - 1
                while optmz["spare"][1] < 0:
                    optmz["spareAdd"][1] -= 1
                    optmz["spare"][1] += optmz["gapAdd"][optmz["deployGold"][1][0]]
                    break
        else:
            optmz["spare"][0] = optmz["spare"][1]
            break
            
    return optmz


def optimizeGate3(optmz):
    for i in range(0, optmz["weeks"] + 1):
        if optmz["spare"][2] > optmz["gapAdd"][optmz["deployGold"][2][0]]:
            if optmz["spare"][2] - optmz["gapAdd"][optmz["deployGold"][2][0]] > 0:
                optmz["spare"][2] = optmz["over"] - (
                    0 if i == 0 else optmz["gapAdd"][optmz["deployGold"][2][0]]
                )
                optmz["spareAdd"][2] = i
                optmz["spare"][1] = optmz["spare"][2]
                optimizeGate2(optmz)
                optmz["spare"][2] = optmz["spare"][1]
                if optmz["gapAdd"][optmz["deployGold"][2][0]] == 0:
                    optmz["spareAdd"][2] = 0
                    break
            else:
                optmz["spareAdd"][2] = i - 1
                while optmz["spare"][2] < 0:
                    optmz["spareAdd"][2] -= 1
                    optmz["spare"][2] += optmz["gapAdd"][optmz["deployGold"][2][0]]
                break
        else:
            optmz["spare"][1] = optmz["spare"][2]
            break


def calcMain(prof, eqmt, raid, opts):
    require = calcRequire(eqmt, raid)
    if opts == None:
        opts = getDefaultOpts(prof, raid, require)
    else:
        opts['require'] = require - opts['inven']
    info = getRaidInfo(raid)
    wPr = getRewardPWeek(info, opts)
    require -= (
        opts["hands"] * wPr[-1]["tReward"] * 2
        + opts["hands"] * (5 if opts["auction"] and opts["entries"][2] != 0 else 0)
        + (20 if opts["fstreward"] else 0)
        + opts['inven']
    )
    if require >= 0:
        weeks = math.ceil(
            require
            / (
                wPr[-1]["tReward"]
                - (
                    (info["reward"][3][1] / (1 if opts["entries"][3] == 3 else 2))
                    if opts["entries"][3] != 0
                    else 0
                )
                + (5 if opts["auction"] and opts["entries"][2] != 0 else 0)
            )
        )
        over = (
            weeks
            * (
                wPr[-1]["tReward"]
                + (5 if opts["auction"] and opts["entries"][2] != 0 else 0)
            )
            - (
                math.trunc(weeks / 2)
                * info["reward"][3][1]
                * (2 if opts["entries"][3] == 3 else 1)
                if opts["entries"][3] != 0
                else 0
            )
            - require
        )
    else:
        while require < 0:
            if (
                require
                + wPr[-1]["tReward"] * 2
                + (5 if opts["auction"] and opts["entries"][2] != 0 else 0)
                < 0
            ):
                opts["hands"] -= 1
                require += wPr[-1]["tReward"] * 2 + (
                    5 if opts["auction"] and opts["entries"][2] != 0 else 0
                )
            else:
                over = (
                    wPr[-1]["tReward"] * 2
                    + (5 if opts["auction"] and opts["entries"][2] != 0 else 0)
                ) * opts["hands"] - opts["require"]
                weeks = 0
                break
    
    if opts["entries"][3] != 0:
        gapAdd = [0 for i in range(len(wPr) - 2)]
    else:
        gapAdd = [0 for i in range(len(wPr) - 1)]
    for i in range(len(gapAdd)):
        if opts["entries"][i] == 1:
            gapAdd[i] = info["reward"][i][0]
        elif opts["entries"][i] == 3:
            gapAdd[i] = info["reward"][i][1]

    spare = [0 for i in range(len(gapAdd))]
    spareAdd = [0 for i in range(len(gapAdd))]
    deployGold = {}

    for i in range(len(gapAdd)):
        deployGold[i] = (
            info["spend"][i][1 if opts["entries"][i] > 2 else 0]
            / info["reward"][i][1 if opts["entries"][i] > 2 else 0]
        )

    deployGold = sorted(deployGold.items(), key=lambda x: x[1], reverse=True)
    spare[-1] = over

    optmz = {
        "weeks": weeks,
        "over": over,
        "gapAdd": gapAdd,
        "deployGold": deployGold,
        "spare": spare,
        "spareAdd": spareAdd,
    }
    if len(gapAdd) == 1:
        optimizeGate1(optmz)    
    elif len(gapAdd) == 2:
        optimizeGate2(optmz)
    else:
        optimizeGate3(optmz)
    marginAdd = {}
    for i in range(len(gapAdd)):
        marginAdd[deployGold[i][0]] = optmz["spareAdd"][i]

    res = []
    accReward = []
    checkGate4 = False
    if weeks == 0:
        rewardResult = (
            opts["require"]
            + over
            + (5 if opts["auction"] and opts["entries"][2] != 0 else 0) * opts["hands"]
        )
    else:
        rewardResult = opts["require"] + optmz["spare"][-1]

    if opts["entries"][3] != 0:
        checkGate4 = True
        if weeks % 2 == 1:
            enterGate4 = True
        else:
            enterGate4 = False

    prevAdd = [i for i in opts["entries"]]
    for i in range(weeks, 0, -1):
        rewardAdd = []
        for idx in range(len(marginAdd)):
            if prevAdd[idx] % 2 == 1:
                if marginAdd[idx] == 0:
                    if opts["entries"][idx] == 1 or opts["entries"][idx] == 2:
                        opts["entries"][idx] = 1
                    elif opts["entries"][idx] == 3 or opts["entries"][idx] == 4:
                        opts["entries"][idx] = 3
                    rewardAdd.append(opts["entries"][idx])
                else:
                    if opts["entries"][idx] == 1 or opts["entries"][idx] == 2:
                        opts["entries"][idx] = 2
                    elif opts["entries"][idx] == 3 or opts["entries"][idx] == 4:
                        opts["entries"][idx] = 4
                    marginAdd[idx] -= 1
                    rewardAdd.append( opts["entries"][idx])
            else:
                rewardAdd.append( opts["entries"][idx])
        if checkGate4:
            if enterGate4:
                opts["entries"][3] = 3 if prevAdd[3] else 4
                rewardAdd.append(prevAdd[3])
                enterGate4 = False
            else:
                opts["entries"][3] = 0
                rewardAdd.append(5)
                enterGate4 = True
        wPr = getRewardPWeek(info, opts)
        accReward.append(
            wPr[-1]["tReward"]+ (5 if opts["auction"] and opts["entries"][2] != 0 else 0)
        )
        if i == weeks:
            res.append(
                {
                    "week": i + opts["hands"],
                    "enter": rewardAdd,
                    "auction": opts["auction"],
                    "material": wPr[-1]["tReward"] + (5 if opts["auction"] and opts["entries"][2] != 0 else 0),
                    "accum": rewardResult,
                    "gold": wPr[-1]["tSpend"],
                    "hands": False,
                }
            )
            rewardResult -= accReward[0]
        elif i == 1 and opts["fstreward"] and opts["hands"] == 0:
            res.append(
                {
                    "week": i + opts["hands"],
                    "enter": rewardAdd,
                    "auction": opts["auction"],
                    "material": str(wPr[-1]["tReward"] + (5 if opts["auction"] and opts["entries"][2] != 0 else 0)) + " + 20",
                    "accum": rewardResult,
                    "gold": wPr[-1]["tSpend"],
                    "hands": False,
                }
            )
            rewardResult -= accReward[0]
        else:
            res.append(
                {
                    "week": i + opts["hands"],
                    "enter": rewardAdd,
                    "auction": opts["auction"],
                    "material": wPr[-1]["tReward"] + (5 if opts["auction"] and opts["entries"][2] != 0 else 0),
                    "accum": rewardResult,
                    "gold": wPr[-1]["tSpend"],
                    "hands": False,
                }
            )
            rewardResult -= accReward[weeks - i]

    for i in range(opts["hands"], 0, -1):
        rewardAdd = []
        for j in range(len(wPr) - 1):
            rewardAdd.append(prevAdd[j])
            opts["entries"] = prevAdd
        wPr = getRewardPWeek(info, opts)
        if weeks > 0:
            # rewardResult-=(5 if opts['auction'] else 0)
            res.append(
                {
                    "week": i,
                    "enter": rewardAdd,
                    "auction": opts["auction"],
                    "material": wPr[-1]["tReward"] * 2  + (5 if opts["auction"] and opts["entries"][2] != 0 else 0),
                    "accum": rewardResult,
                    "gold": wPr[-1]["tSpend"]
                    + (50 if opts["auction"] and opts["entries"][2] != 0 else 0),
                    "hands": True,
                }
            )
            rewardResult -= wPr[-1]["tReward"] * 2 + (
                5 if opts["auction"] and opts["entries"][2] != 0 else 0
            )
            weeks = 0
        elif i == 1 and opts["fstreward"]:
            res.append(
                {
                    "week": i,
                    "enter": rewardAdd,
                    "auction": opts["auction"],
                    "material": str( wPr[-1]["tReward"] * 2  + (5 if opts["auction"] and opts["entries"][2] != 0 else 0))+" + 20",
                    "accum": rewardResult,
                    "gold": wPr[-1]["tSpend"]
                    + (50 if opts["auction"] and opts["entries"][2] != 0 else 0),
                    "hands": True,
                }
            )
            rewardResult -= wPr[-1]["tReward"] * 2 + (
                5 if opts["auction"] and opts["entries"][2] != 0 else 0
            )
        else:
            res.append(
                {
                    "week": i,
                    "enter": rewardAdd,
                    "auction": opts["auction"],
                    "material": wPr[-1]["tReward"] * 2   + (5 if opts["auction"] and opts["entries"][2] != 0 else 0),
                    "accum": rewardResult,
                    "gold": wPr[-1]["tSpend"]
                    + (50 if opts["auction"] and opts["entries"][2] != 0 else 0),
                    "hands": True,
                }
            )
            rewardResult -= wPr[-1]["tReward"] * 2 + (
                5 if opts["auction"] and opts["entries"][2] != 0 else 0
            )

    return {"res":res,"opts":opts}
