import json

achive = "achive.json"
dress = "dress.json"
land = "land.json"
level = "level.json"
libao = "libao.json"
load = "load.json"
lucky = "lucky.json"
Message = "Message.json"
onLine = "onLine.json"
personDefaultDress = "personDefaultDress.json"
personSpine = "personSpine.json"
renwu = "renwu.json"
ResPath = "ResPath.json"
sceneSel = "sceneSel.json"
seed = "seed.json"
sign = "sign.json"
store = "store.json"
store_guonei = "store_guonei.json"
suit = "suit.json"
suitPet = "suitPet.json"
themeModel = "themeModel.json"
themeModelReward = "themeModelReward.json"
UITexture = "UITexture.json"
yaoshui = "yaoshui.json"


def initCon(path):
    f = open("Server/WebSocket/model/json/" + path + "", encoding='utf-8')
    data = json.load(f)
    f.close()
    tmpdata = {}

    _indexstr = 'id'

    if (path == "level.json"):
        _indexstr = "level"

    for values in data:
        tmpkey = int(values[_indexstr])
        tmpdata[tmpkey] = values
    return tmpdata


def init():
    pass


achive_Data = initCon(achive)
dress_Data = initCon(dress)
land_Data = initCon(land)
level_Data = initCon(level)
libao_Data = initCon(libao)
load_Data = initCon(load)
lucky_Data = initCon(lucky)
Message_Data = initCon(Message)
onLine_Data = initCon(onLine)
# personDefaultDress_Data = initCon(personDefaultDress)
# personSpine_Data = initCon(personSpine)
renwu_Data = initCon(renwu)
# ResPath_Data = initCon(ResPath)
sceneSel_Data = initCon(sceneSel)
seed_Data = initCon(seed)
sign_Data = initCon(sign)
store_Data = initCon(store)
# store_guonei_Data = initCon(store_guonei)
suit_Data = initCon(suit)

# print(achive_Data)
# suitPet_Data = initCon(suitPet)
# themeModel_Data = initCon(themeModel)
# themeModelReward_Data = initCon(themeModelReward)
# UITexture_Data = initCon(UITexture)
# yaoshui_Data = initCon(yaoshui)


def GetMsgstr(id):
    _data = Message_Data[id]
    if (_data != None):
        return _data["info_cn"]


A_S_suitlistid = []

for _val in suit_Data.values():
    if (_val["fame"] == 3 or _val["fame"] == 4):
        A_S_suitlistid.append(_val["id"])
print(A_S_suitlistid)
# 钻石商店消耗和增加数据
shoplist3_con = [[19.9, 1400], [0.99, 60], [2.99, 200], [4.99, 340], [9.99, 740]]
# 金币商店消耗和增加数据
shoplist4_con = [[1000, 120000], [10, 600], [60, 4000], [200, 15000], [400, 35000]]

# 免费商店
free_shop = [[1010, 2, 3], [1011, 2, 3], [1019, 2, 3], [1027, 2, 3]]

# 种子商店限时种子
# seed_shop = []
