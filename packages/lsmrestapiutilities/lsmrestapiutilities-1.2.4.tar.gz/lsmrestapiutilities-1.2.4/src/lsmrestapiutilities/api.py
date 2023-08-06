from .consts import URL
from riotapiutilities.api import RiotApi
from riotapiutilities.consts import REGIONS

import requests

class RESTAPI :
    def __init__(self, api_key) :
        self.api_key = api_key
    
    def request_get(self, api_url, params={}) :
        args = {'Authorization' : self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.get(
            URL['base'].format(
                url=api_url
            ),
            headers=args
        )
        
        return response.json()

    def request_post(self, api_url, body, params={}) :
        args = {'Authorization' : self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.post(
            URL['base'].format(
                url=api_url
            ),
            data=body,
            headers=args
        )
        
        return response.json()

    def request_update(self, api_url, body, params={}) :
        args = {'Authorization' : self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.put(
            URL['base'].format(
                url=api_url
            ),
            data=body,
            headers=args
        )

        return response.json()

    def custom_filtered_request_get(self, endpoint, filter) :
        api_url = URL[endpoint].format(url=filter)
        return self.request_get(api_url)

    def custom_request_get(self, url) :
        api_url = URL['base'].format(url=url)
        return self.request_get(api_url)



    def get_summoner_by_name(self, summoner_name) :
        api_url = URL['summoners'].format(url='?name={name}'.format(name=summoner_name))
        return self.request_get(api_url)

    def get_summoner_by_id(self, id) :
        api_url = URL['summoners'].format(url='?id={id}'.format(id=id))
        return self.request_get(api_url)

    def get_summoner_by_account_id(self, account_id) :
        api_url = URL['summoners'].format(url='?accountid={id}'.format(id=account_id))
        return self.request_get(api_url)

    def get_summoner_by_puuid(self, puuid) :
        api_url = URL['summoners'].format(url='?puuid={id}'.format(id=puuid))
        return self.request_get(api_url)

    def get_summoner_by_level(self, level) :
        api_url = URL['summoners'].format(url='?summonerlevel={level}'.format(level=level))
        return self.request_get(api_url)


    
    def get_map_by_id(self, id) :
        api_url = URL['maps'].format(url='?mapid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_map_by_name(self, name) :
        api_url = URL['maps'].format(url='?mapname={name}'.format(name=name))
        return self.request_get(api_url)



    def get_rune_by_id(self, id) :
        api_url = URL['runes'].format(url='?runeid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_rune_by_name(self, name) :
        api_url = URL['runes'].format(url='?name={name}'.format(name=name))
        return self.request_get(api_url)

    def get_rune_by_style(self, style) :
        api_url = URL['runes'].format(url='?style={style}'.format(style=style))
        return self.request_get(api_url)



    def get_runestyle_by_id(self, id) :
        api_url = URL['runestyles'].format(url='?styleid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_runestyle_by_name(self, name) :
        api_url = URL['runestyles'].format(url='?name={name}'.format(name=name))
        return self.request_get(api_url)



    def get_queue_by_id(self, id) :
        api_url = URL['queues'].format(url='?queueid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_queue_by_map(self, map) :
        api_url = URL['queues'].format(url='?map={map}'.format(map=map))
        return self.request_get(api_url)

    

    def get_champion_by_id(self, id) :
        api_url = URL['champions'].format(url='?championid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_champion_by_name(self, name) :
        api_url = URL['champions'].format(url='?name={name}'.format(name=name))
        return self.request_get(api_url)



    def get_championmastery_by_summonerid(self, summonerid) :
        api_url = URL['championmasteries'].format(url='?summonerid={id}'.format(id=summonerid))
        return self.request_get(api_url)

    def get_championmastery_by_championid(self, championid) :
        api_url = URL['championmasteries'].format(url='?championid={id}'.format(id=championid))
        return self.request_get(api_url)



    def get_league_by_leagueid(self, leagueid) :
        api_url = URL['leagues'].format(url='?leagueid={id}'.format(id=leagueid))
        return self.request_get(api_url)

    def get_league_by_queue(self, queue) :
        api_url = URL['leagues'].format(url='?queuetype={queue}'.format(queue=queue))
        return self.request_get(api_url)

    def get_league_by_tier(self, tier) :
        api_url = URL['leagues'].format(url='?tier={tier}'.format(tier=tier))
        return self.request_get(api_url)

    def get_league_by_rank(self, rank) :
        api_url = URL['leagues'].format(url='?rank={rank}'.format(rank=rank))
        return self.request_get(api_url)

    def get_league_by_summonerid(self, summonerid) :
        api_url = URL['leagues'].format(url='?summonerid={id}'.format(id=summonerid))
        return self.request_get(api_url)

    def get_league_by_summonername(self, summonername) :
        api_url = URL['leagues'].format(url='?summonername={name}'.format(name=summonername))
        return self.request_get(api_url)

    

    def get_item_by_id(self, id) :
        api_url = URL['items'].format(url='?itemid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_item_by_name(self, name) :
        api_url = URL['items'].format(url='?name={name}'.format(name=name))
        return self.request_get(api_url)


    
    def get_match_by_id(self, id) :
        api_url = URL['matches'].format(url='?matchid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_match_by_mapid(self, mapid) :
        api_url = URL['matches'].format(url='?mapid={id}'.format(id=mapid))
        return self.request_get(api_url)

    def get_match_by_queueid(self, queueid) :
        api_url = URL['matches'].format(url='?queueid={id}'.format(id=queueid))
        return self.request_get(api_url)

    def get_match_by_gameversion(self, gameversion) :
        api_url = URL['matches'].format(url='?gameversion={version}'.format(version=gameversion))
        return self.request_get(api_url)

    def get_match_by_gamemode(self, gamemode) :
        api_url = URL['matches'].format(url='?gamemode={mode}'.format(mode=gamemode))
        return self.request_get(api_url)

    def get_match_by_gamename(self, gamename) :
        api_url = URL['matches'].format(url='?gamename={name}'.format(name=gamename))
        return self.request_get(api_url)

    

    def get_matchteam_by_matchid(self, id) :
        api_url = URL['matchteams'].format(url='?matchid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_matchteam_by_teamid(self, teamid) :
        api_url = URL['matchteams'].format(url='?teamid={id}'.format(id=teamid))
        return self.request_get(api_url)

    def get_matchteam_by_matchid_and_teamid(self, id, teamid) :
        api_url = URL['matchteams'].format(url='?matchid={id}&teamid={teamid}'.format(id=id, teamid=teamid))
        return self.request_get(api_url)

    

    def get_matchparticipant_by_matchid(self, matchid) :
        api_url = URL['matchparticipants'].format(url='?matchid={id}'.format(id=matchid))
        return self.request_get(api_url)

    def get_matchparticipant_by_summonerid(self, summonerid) :
        api_url = URL['matchparticipants'].format(url='?summonerid={id}'.format(id=summonerid))
        return self.request_get(api_url)

    def get_matchparticipant_by_puuid(self, puuid) :
        api_url = URL['matchparticipants'].format(url='?puuid={id}'.format(id=puuid))
        return self.request_get(api_url)

    def get_matchparticipant_by_matchid_and_summonerid(self, matchid, summonerid) :
        api_url = URL['matchparticipants'].format(url='?matchid={id}&summonerid={summonerid}'.format(id=matchid, summonerid=summonerid))
        return self.request_get(api_url)

    def get_matchparticipant_by_matchid_and_puuid(self, matchid, puuid) :
        api_url = URL['matchparticipants'].format(url='?matchid={id}&puuid={puuid}'.format(id=matchid, puuid=puuid))
        return self.request_get(api_url)

    

    def get_summonerspell_by_key(self, key) :
        api_url = URL['summonerspells'].format(url='?spellkey={key}'.format(key=key))
        return self.request_get(api_url)

    def get_summonerspell_by_id(self, id) :
        api_url = URL['summonerspells'].format(url='?spellid={id}'.format(id=id))
        return self.request_get(api_url)

    def get_summonerspell_by_name(self, name) :
        api_url = URL['summonerspells'].format(url='?name={name}'.format(name=name))
        return self.request_get(api_url)

    

    def post_summoner(self, summoner) : 
        body = {
            'id' : summoner['id'],
            'accountid' : summoner['accountId'],
            'puuid' : summoner['puuid'],
            'name' : summoner['name'],
            'profileiconid' : summoner['profileIconId'],
            'revisiondate' : summoner['revisionDate'],
            'summonerlevel' : summoner['summonerLevel']
        }
        api_url = URL['summoners'].format(url='/')
        return self.request_update(api_url, body)

    def post_match(self, match) :
        body = {
            'matchid' : match['metadata']['matchId'],
            'gamemode' : '{mode}'.format(mode=match['info']['gameMode']),
            'gameduration' : match['info']['gameDuration'],
            'gamename' : match['info']['gameName'],
            'gametype' : match['info']['gameType'],
            'mapid' : match['info']['mapId'],
            'queueid' : match['info']['queueId'],
            'platformid' : match['info']['platformId'],
            'gameversion' : '{version}'.format(version=match['info']['gameVersion']),
            'gamecreation' : match['info']['gameCreation'],
            'gameendtimestamp' : match['info']['gameEndTimestamp'],
            'gamestarttimestamp' : match['info']['gameStartTimestamp']
        }
        api_url = URL['matches'].format(url='/')
        return self.request_post(api_url, body)

    def post_matchTeams(self, match) :
        matchid = match['metadata']['matchId']
        for team in match['info']['teams'] :
            teamid = team['teamId']
            response = self.get_matchteam_by_matchid_and_teamid(matchid, teamid)
            if match['info']['gameMode'] == 'ARAM' :
                ban1, ban2, ban3, ban4, ban5 = -1, -1, -1, -1, -1
            else :
                ban1 = team['bans'][0]['championId']
                ban2 = team['bans'][1]['championId']
                ban3 = team['bans'][2]['championId']
                ban4 = team['bans'][3]['championId']
                ban5 = team['bans'][4]['championId']
            body = {
                'matchid' : matchid,
                'teamid' : teamid,
                'win' : team['win'],
                'ban1' : ban1,
                'ban2' : ban2,
                'ban3' : ban3,
                'ban4' : ban4,
                'ban5' : ban5,
                'firstbaron' : team['objectives']['baron']['first'],
                'baronkills' : team['objectives']['baron']['kills'],
                'firstchampion' : team['objectives']['champion']['first'],
                'championkills' : team['objectives']['champion']['kills'],
                'firstdragon' : team['objectives']['dragon']['first'],
                'dragonkills' : team['objectives']['dragon']['kills'],
                'firstinhibitor' : team['objectives']['inhibitor']['first'],
                'inhibitorkills' : team['objectives']['inhibitor']['kills'],
                'firstriftherald' : team['objectives']['riftHerald']['first'],
                'riftheraldkills' : team['objectives']['riftHerald']['kills'],
                'firsttower' : team['objectives']['tower']['first'],
                'towerkills' : team['objectives']['tower']['kills']
            }
            if (len(response) == 0) :
                api_url = URL['matchteams'].format(url='/')
                self.request_post(api_url, body)
            else :
                api_url = URL['matchteams'].format(url='/{id}'.format(id=response[0]['id']))
                self.request_update(api_url, body)

        return True

    def post_matchParticipants(self, match) :
        for participant in match['info']['participants'] : 
            styles = []
            runes = []

            for style in participant['perks']['styles'] :
                styles.append(style['style'])
            for style in participant['perks']['styles'] :
                for selection in style['selections'] :
                    runes.append(selection['perk'])
            puuid = participant['puuid']
            RIOT_KEY = 'RGAPI-ef3247df-953a-4361-80f7-f3f2c255b5d0'
            summoner = RiotApi(RIOT_KEY, REGIONS['north_america']).get_summoner_by_puuid(puuid)
            self.post_summoner(summoner)
            body = {
                "matchid" : "{matchId}".format(matchId=match['metadata']['matchId']),
                "summonerid" : "{summonerId}".format(summonerId=participant['summonerId']),
                "assists" : int(participant['assists']),
                "baronkills" : int(participant['baronKills']),
                "champexperience" : int(participant['champExperience']),
                "champlevel" : int(participant['champLevel']),
                "championid" : int(participant['championId']),
                "championname" : "{championName}".format(championName=participant['championName']),
                "damagedealttobuildings" : int(participant['damageDealtToBuildings']),
                "damagedealttoobjectives" : int(participant['damageDealtToObjectives']),
                "damagedealttoturrets" : int(participant['damageDealtToTurrets']),
                "damageselfmitigated" : int(participant['damageSelfMitigated']),
                "deaths" : int(participant['deaths']),
                "gameendedinsurrender" : participant['gameEndedInSurrender'],
                "goldearned" : int(participant['goldEarned']),
                "goldspent" : int(participant['goldSpent']),
                "individualposition" : "{individualPosition}".format(individualPosition=participant['individualPosition']),
                "item0" : int(participant['item0']),
                "item1" : int(participant['item1']),
                "item2" : int(participant['item2']),
                "item3" : int(participant['item3']),
                "item4" : int(participant['item4']),
                "item5" : int(participant['item5']),
                "item6" : int(participant['item6']),
                "kills" : int(participant['kills']),
                "lane" : "{lane}".format(lane=participant['lane']),
                "magicdamagedealt" : int(participant['magicDamageDealt']),
                "magicdamagedealttochampions" : int(participant['magicDamageDealtToChampions']),
                "participantid" : int(participant['participantId']),
                "physicaldamagedealt" : int(participant['physicalDamageDealt']),
                "physicaldamagedealttochampions" : int(participant['physicalDamageDealtToChampions']),
                "profileiconid" : int(participant['profileIcon']),
                "puuid" : puuid,
                "riotidname" : "{riotIdName}".format(riotIdName=participant['riotIdName']),
                "riotidtagline" : "{riotIdTagline}".format(riotIdTagline=participant['riotIdTagline']),
                "role" : "{role}".format(role=participant['role']),
                "rune1id" : int(runes[0]),
                "rune2id" : int(runes[1]),
                "rune3id" : int(runes[2]),
                "rune4id" : int(runes[3]),
                "rune5id" : int(runes[4]),
                "rune6id" : int(runes[5]),
                "runestyle1id" : int(styles[0]),
                "runestyle2id" : int(styles[1]),
                "summoner1id" : int(participant['summoner1Id']),
                "summoner2id" : int(participant['summoner2Id']),
                "summonerlevel" : int(participant['summonerLevel']),
                "summonername" : "{summonerName}".format(summonerName=participant['summonerName']),
                "teamearlysurrendered" : participant['teamEarlySurrendered'],
                "teamid" : int(participant['teamId']),
                "teamposition" : "{teamPosition}".format(teamPosition=participant['teamPosition']),
                "totaldamagedealt" : int(participant['totalDamageDealt']),
                "totaldamagedealttochampions" : int(participant['totalDamageDealtToChampions']),
                "totalheal" : int(participant['totalHeal']),
                "totalminionskilled" : int(participant['totalMinionsKilled']),
                "truedamagedealt" : int(participant['trueDamageDealt']),
                "truedamagedealttochampions" : int(participant['trueDamageDealtToChampions']),
                "win" : participant['win']
            }
        
            response = self.get_matchparticipant_by_matchid_and_puuid(match['metadata']['matchId'], puuid)
            if (len(response) == 0) :
                api_url=URL['matchparticipants'].format(url='/')
                self.request_post(api_url, body)
            else :
                api_url=URL['matchparticipants'].format(url='/'+str(response[0]['id']))
                self.request_update(api_url, body)
        return True

    def post_league(self, leagues) :
        for league in leagues :
            if league['queueType'] == 'RANKED_TFT_PAIRS' :
                pass
            else :
                body = {
                    'leagueid' : league['leagueId'],
                    'queuetype' : league['queueType'],
                    'tier' : league['tier'],
                    'rank' : league['rank'],
                    'summonerid' : league['summonerId'],
                    'summonername' : league['summonerName'],
                    'leaguepoints' : league['leaguePoints'],
                    'wins' : league['wins'],
                    'losses' : league['losses'],
                    'veteran' : league['veteran'],
                    'inactive': league['inactive'],
                    'freshblood' : league['freshBlood'],
                    'hotstreak' : league['hotStreak']
                }

                api_url = URL['leagues'].format(url='/')
                self.request_post(api_url, body)

        return True

    def post_championMastery(self, championMastery) : 
        body = {
            'summonerid' : championMastery['summonerId'],
            'championid' : championMastery['championId'],
            'championlevel' : championMastery['championLevel'],
            'championpoints' : championMastery['championPoints'],
            'championpointssincelastlevel' : championMastery['championPointsSinceLastLevel'],
            'championpointsuntilnextlevel' : championMastery['championPointsUntilNextLevel'],
            'chestgranted' : championMastery['chestGranted'],
            'tokensearned' : championMastery['tokensEarned']
        }
        
        api_url = URL['championmasteries'].format(url='/')
        return self.request_post(api_url, body)

    def post_all_match_data(self, match) : 
        self.post_match(match)
        self.post_matchTeams(match)
        self.post_matchParticipants(match)
        return True