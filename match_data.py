import requests
from requests.exceptions import RequestException
import json
from json.decoder import JSONDecodeError
import pymongo
from multiprocessing import Pool

MONGO_URL = 'localhost'
MONGO_DB = 'lol_match3'
MONGO_TABLE = 'items'
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'wp_pvid=2207694495; wp_info=ssid=s7774711643; isShown=1; gameType=2; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1501834517,1502713016; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1502714406; wanplus_token=bdb6fd5663f1ae71bbf734fc154ddac9; wanplus_storage=lvpysLf1ayyiKxm9zzaQmLnMA%2FK%2FryXBdJYx1QOk4cC344W4wvbTHyM5htE7H%2BhRKLE9zwNsxT4hSYMvwI%2F04tizp3esiOFnuaiefVSDLvRzzmvP%2BvZn22c; wanplus_sid=267686cb7492348ed800074c6d60bb2e; wanplus_csrf=_csrf_tk_1792768770',
    'Host':'www.wanplus.com',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
    'X-CSRF-Token':'1809545986',
    'X-Requested-With':'XMLHttpRequest',
}
#打开单场比赛索引页
def get_page_index(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

#解析单场比赛数据
def parse_page_index(html):
    try:
        data = json.loads(html)
        for i in range(2):
            if i == 0:
                color = 'blue'
            else:
                color = 'red'
            for j in range(5):
                x = str(j + 1)
                json1 = data.get('data').get('plList')[i].get(x)
                json2 = json1.get('stats')
                json3 = data.get('data').get('info')

                gameversion = json3.get('gameversion')  # 游戏版本
                blueid = json3.get('oneteam').get('teamid')  # 蓝色方队伍id
                bluename = json3.get('oneteam').get('teamalias')  # 蓝色方队伍名称
                redid = json3.get('twoteam').get('teamid')  # 红色方队伍id
                redname = json3.get('twoteam').get('teamalias')  # 红色方队伍名称
                duration = json3.get('duration')  # 游戏时长
                matchorder = json3.get('matchorder')  # 游戏场次
                winid = json3.get('winner')  # 胜利方队伍id
                gametype = json3.get('gametype')  # 比赛类型bo几

                baron1 = data.get('data').get('teamStatsList').get('baronkills')[0]  # 蓝色方男爵击杀次数
                baron2 = data.get('data').get('teamStatsList').get('baronkills')[1]  # 红色方男爵击杀次数
                dragon1 = data.get('data').get('teamStatsList').get('dragonkills')[0]  # 蓝色方小龙击杀次数
                dragon2 = data.get('data').get('teamStatsList').get('dragonkills')[1]  # 红色方小龙击杀次数

                scheduleid = data.get('data').get('plList')[0].get('1').get('scheduleid')  # 比赛id
                matchid = data.get('data').get('plList')[0].get('1').get('matchid')  # 单场id

                ban = data.get('data').get('bpList').get('bans')[i][j].get('cpherokey')  # ban人
                pick = json1.get('cpherokey')  # 选择英雄

                lane = json1.get('lane')  # 位置
                kda = json1.get('kda')  # kda
                playername = json1.get('playername')  # 选手名称
                playerid = json1.get('playerid')  # 选手id

                assists = json2.get('assists')  # 助攻数
                deaths = json2.get('deaths')  # 死亡数
                doubleKills = json2.get('doubleKills')  # 双杀次数
                firstBloodAssist = json2.get('firstBloodAssist')  # 是否助攻一血
                firstBloodKill = json2.get('firstBloodKill')  # 是否拿下一血
                firstTowerAssist = json2.get('firstTowerAssist')  # 是否助攻一塔
                firstTowerKill = json2.get('firstTowerKill')  # 是否拿下一塔
                goldEarned = json2.get('goldEarned')  # 金钱数
                goldSpent = json2.get('goldSpent')  # 花钱数
                killingSprees = json2.get('killingSprees')  # 杀人如麻次数
                kills = json2.get('kills')  # 击杀数
                largestKillingSpree = json2.get('largestKillingSpree')  # 最大杀人如麻次数
                largestMultiKill = json2.get('largestMultiKill')  # 最大连杀数
                magicDamageDealt = json2.get('magicDamageDealt')  # 造成的魔法伤害
                magicDamageDealtToChampions = json2.get('magicDamageDealtToChampions')  # 对英雄造成的魔法伤害
                magicDamageTaken = json2.get('magicDamageTaken')  # 承受的魔法伤害
                minionsKilled = json2.get('minionsKilled')  # 补刀数
                neutralMinionsKilledEnemyJungle = json2.get('neutralMinionsKilledEnemyJungle')  # 敌方野怪击杀数
                neutralMinionsKilledTeamJungle = json2.get('neutralMinionsKilledTeamJungle')  # 己方野怪击杀数
                physicalDamageDealt = json2.get('physicalDamageDealt')  # 造成的物理伤害
                physicalDamageDealtToChampions = json2.get('physicalDamageDealtToChampions')  # 对英雄造成的物理伤害
                physicalDamageTaken = json2.get('physicalDamageTaken')  # 承受的物理伤害
                totalDamageDealt = json2.get('totalDamageDealt')  # 造成的总伤害
                totalDamageDealtToChampions = json2.get('totalDamageDealtToChampions')  # 对英雄造成的总伤害
                totalDamageTaken = json2.get('totalDamageTaken')  # 承受的总伤害
                totalHeal = json2.get('totalHeal')  # 治疗量
                trueDamageDealt = json2.get('trueDamageDealt')  # 造成的真实伤害
                trueDamageDealtToChampions = json2.get('trueDamageDealtToChampions')  # 对英雄造成的真实伤害
                trueDamageTaken = json2.get('trueDamageTaken')  # 承受的真实伤害
                items = {
                    'gameversion': gameversion,
                    'blueid': blueid,
                    'bluename': bluename,
                    'redid': redid,
                    'redname': redname,
                    'duration': duration,
                    'winid': winid,
                    'gametype': gametype,
                    'scheduleid': scheduleid,
                    'matchid': matchid,
                    'baron1': baron1,
                    'baron2': baron2,
                    'dragon1': dragon1,
                    'dragon2': dragon2,
                    'color': color,
                    'ban': ban,
                    'x': x,
                    'pick': pick,
                    'lane': lane,
                    'kda': kda,
                    'playername': playername,
                    'playerid': playerid,
                    'assists': assists,
                    'deaths': deaths,
                    'doubleKills': doubleKills,
                    'firstBloodAssist': firstBloodAssist,
                    'firstBloodKill': firstBloodKill,
                    'firstTowerAssist': firstTowerAssist,
                    'firstTowerKill': firstTowerKill,
                    'goldEarned': goldEarned,
                    'goldSpent': goldSpent,
                    'killingSprees': killingSprees,
                    'kills': kills,
                    'largestKillingSpree': largestKillingSpree,
                    'largestMultiKill': largestMultiKill,
                    'magicDamageDealt': magicDamageDealt,
                    'magicDamageDealtToChampions': magicDamageDealtToChampions,
                    'magicDamageTaken': magicDamageTaken,
                    'minionsKilled': minionsKilled,
                    'neutralMinionsKilledEnemyJungle': neutralMinionsKilledEnemyJungle,
                    'neutralMinionsKilledTeamJungle': neutralMinionsKilledTeamJungle,
                    'physicalDamageDealt': physicalDamageDealt,
                    'physicalDamageDealtToChampions': physicalDamageDealtToChampions,
                    'physicalDamageTaken': physicalDamageTaken,
                    'totalDamageDealt': totalDamageDealt,
                    'totalDamageDealtToChampions': totalDamageDealtToChampions,
                    'totalDamageTaken': totalDamageTaken,
                    'totalHeal': totalHeal,
                    'trueDamageDealt': trueDamageDealt,
                    'trueDamageDealtToChampions': trueDamageDealtToChampions,
                    'trueDamageTaken': trueDamageTaken
                }
                save_to_mongo(items)
                print(items)
    except JSONDecodeError :
        print('JSONDecodeError')
        pass

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到mongod成功',result)
    except Exception:
        print('存储到monggodb失败',result)

def write_to_file(content):
    with open('lol_match.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def main(num):
        print(num)
        html = get_page_index('https://www.wanplus.com/ajax/matchdetail/'+str(num)+'?_gtk=1809545986')
        try:
            parse_page_index(html)
        except AttributeError:
            pass
        except IndexError:
            pass
        except TypeError:
            pass

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(39781,41000)])
    pool.close()
    pool.join()

