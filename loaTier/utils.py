class StaticResult:
    def __init__(self, ndata, data, tier_Cnt, engv_Pick):
        self.n = ndata
        self.data = data
        self.tPe = tier_Cnt
        self.pick = engv_Pick
    
    # 각인 dictionary
    engvName = {
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
    # 티어 dictionary
    tierName = {"tier1":'', "tier2":'', "tier3":'', "tier4":'', "tier5":'', "tierout":''}
    
    def getEngv():
        res = {
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
        return res
    
    def getTier():
        res = {"tier1":'', "tier2":'', "tier3":'', "tier4":'', "tier5":'', "tierout":''}
        return res

    def tierPerEngv(n, data):
        res = StaticResult.getTier()
        for tn in StaticResult.tierName.keys():
            res[tn] = StaticResult.getEngv()

        for loop in range(n):
            for tn in StaticResult.tierName.keys():
                for en in StaticResult.engvName.keys():
                    if data[tn].str.contains(en)[loop]:
                        res[tn][en] +=1
        return res

    def getEngvPick(tPe):
        
        idx = 0
        temp = StaticResult.getTier()
        for tn in StaticResult.tierName.keys():
            temp[tn] = list(tPe[tn].values())

        pick = list()
        for a,b,c,d,e,f in zip(temp['tier1'],temp['tier2'],temp['tier3'],temp['tier4'],temp['tier5'],temp['tierout']):
            pick.append(a+b+c+d+e)
        res = StaticResult.getEngv()
        for en in StaticResult.engvName.keys():
            res[en] = pick[idx]
            idx +=1

        return res

    def getEngvStatics(n, tPe,pick):
        res = StaticResult.getEngv()
        for en in StaticResult.engvName.keys():
            res[en] = {"OP": 0, "1티어": 0, "2티어": 0, "3티어": 0, "4티어": 0, "선택없음": 0}
            if pick[en] != 0:
                for tn in ["OP", "1티어", "2티어", "3티어", "4티어"]:
                    res[en][tn] = tPe[tn][en] / pick[en]
                    res[en]["선택없음"] = n-pick[en]
            else:
                res[en]["선택없음"] = n
        return res
    
    def getEngvScore(tPe, pick):
        score = StaticResult.getEngv()
        for tn in StaticResult.tierName.keys():
            for en in StaticResult.engvName.keys():
                if pick[en] != 0:
                    if tn == "tier1" :
                        score[en] += (tPe[tn][en]*5)/pick[en]
                    elif tn == "tier2":
                        score[en] += (tPe[tn][en]*4)/pick[en]
                    elif tn == "tier3":
                        score[en] += (tPe[tn][en]*3)/pick[en]
                    elif tn == "tier4":
                        score[en] += (tPe[tn][en]*2)/pick[en]
                    elif tn == "tier5":
                        score[en] += (tPe[tn][en])/pick[en]
        # 점수를 큰 순서대로 정렬
        score = sorted(score.items(), key=lambda item: item[1], reverse=True)
        
        res ={
            "tier1": [],
            "tier2": [],
            "tier3": [],
            "tier4": [],
            "tier5": [],
            "tierout": [],
        }

        for x, y in score:
            if y > 4.0:
                res["tier1"] += [x]
            elif y > 3.0:
                res["tier2"] += [x]
            elif y > 2.0:
                res["tier3"] += [x]
            elif y > 1.0:
                res["tier4"] += [x]
            elif y > 0:
                res["tier5"] += [x]
            else:
                res["tierout"] += [x]
        return res