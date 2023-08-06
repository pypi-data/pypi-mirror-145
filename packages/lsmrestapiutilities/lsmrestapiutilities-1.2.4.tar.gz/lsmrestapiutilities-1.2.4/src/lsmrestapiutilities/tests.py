from api import RESTAPI
from riotapiutilities import api
from riotapiutilities import consts

api_conn = RESTAPI('Token a7cb48f9a0645e2eb18ea44795907fb7be41dc58')

key = 'RGAPI-ef3247df-953a-4361-80f7-f3f2c255b5d0'
na1_api = api.RiotApi(key, consts.REGIONS['north_america'])
americas_api = api.RiotApi(key, consts.REGIONS['americas'])

# print(api_conn.get_summoner_by_name('FunnyBug'))
# print(api_conn.get_summoner_by_account_id('CXEI5Ga72gLJwkLwja6_PFkc1moog-wiIhrCBjucF-d9AaM'))
# print(api_conn.get_summoner_by_id('335Zf1OEWrsPVV-lWYz9j3iyD_5NOhwsf9Bu0onIIB8qRIo'))
# print(api_conn.get_summoner_by_puuid('kLjXwJiAA8MRLJjE_bBowZtGLiUL-nSieGTh9XIqk9wECAM4EGIDQSItZ2YVKDjbHZSYeazDAIcLhg'))
# print(api_conn.get_summoner_by_level('108'))

# print(api_conn.get_map_by_id('1'))
# print(api_conn.get_map_by_name('Summoners Rift'))

# print(api_conn.get_rune_by_id('8005'))
# print(api_conn.get_rune_by_name('Press the Attack'))
# print(api_conn.get_rune_by_style('8000'))

# print(api_conn.get_runestyle_by_id('8000'))
# print(api_conn.get_runestyle_by_name('Precision'))

# print(api_conn.get_queue_by_id('0'))
# print(api_conn.get_queue_by_map('Summoners Rift'))

# print(api_conn.get_champion_by_id('1'))
# print(api_conn.get_champion_by_name('Annie'))

# print(api_conn.get_championmastery_by_championid('1'))
# print(api_conn.get_championmastery_by_summonerid('335Zf1OEWrsPVV-lWYz9j3iyD_5NOhwsf9Bu0onIIB8qRIo'))

# print(api_conn.get_league_by_leagueid('1'))
# print(api_conn.get_league_by_queue('0'))
# print(api_conn.get_league_by_rank('I'))
# print(api_conn.get_league_by_tier('GOLD'))
# print(api_conn.get_league_by_summonerid('335Zf1OEWrsPVV-lWYz9j3iyD_5NOhwsf9Bu0onIIB8qRIo'))
# print(api_conn.get_league_by_summonername('FunnyBug'))

# print(api_conn.get_item_by_id('1001'))
# print(api_conn.get_item_by_name('Boots'))

# print(api_conn.get_match_by_id('NA1_4243491999'))
# print(api_conn.get_match_by_mapid(11))
# print(api_conn.get_match_by_queueid(400))
# print(api_conn.get_match_by_gameversion('12.5.425.9171'))
# print(api_conn.get_match_by_gamemode('CLASSIC'))
# print(api_conn.get_match_by_gamename('teambuilder-match-4243491999'))

# print(api_conn.get_matchteam_by_matchid('NA1_4243491999'))
# print(api_conn.get_matchteam_by_teamid('100'))
# print(api_conn.get_matchteam_by_matchid_and_teamid('NA1_4243491999', '100'))

# print(api_conn.get_matchparticipant_by_matchid('NA1_4243491999'))
# print(api_conn.get_matchparticipant_by_summonerid('335Zf1OEWrsPVV-lWYz9j3iyD_5NOhwsf9Bu0onIIB8qRIo'))
# print(api_conn.get_matchparticipant_by_puuid('kLjXwJiAA8MRLJjE_bBowZtGLiUL-nSieGTh9XIqk9wECAM4EGIDQSItZ2YVKDjbHZSYeazDAIcLhg'))
# print(api_conn.get_matchparticipant_by_matchid_and_summonerid('NA1_4243491999', '335Zf1OEWrsPVV-lWYz9j3iyD_5NOhwsf9Bu0onIIB8qRIo'))
# print(api_conn.get_matchparticipant_by_matchid_and_puuid('NA1_4243491999', 'kLjXwJiAA8MRLJjE_bBowZtGLiUL-nSieGTh9XIqk9wECAM4EGIDQSItZ2YVKDjbHZSYeazDAIcLhg'))

# print(api_conn.get_summonerspell_by_key('1'))
# print(api_conn.get_summonerspell_by_id('SummonerExhaust'))
# print(api_conn.get_summonerspell_by_name('Smite'))

# print(na1_api.get_summoner_by_name('FunnyBug'))
# print(api_conn.post_summoner(na1_api.get_summoner_by_name('FunnyBug')))

# print (api_conn.post_all_match_data(americas_api.get_match_by_match_id('NA1_4243491999')))
# print(api_conn.post_matchTeams(americas_api.get_match_by_match_id('NA1_4243491999')))
# print(api_conn.post_matchParticipants(americas_api.get_match_by_match_id('NA1_4243491999')))
# print(api_conn.post_league(na1_api.get_league_by_summoner_id('335Zf1OEWrsPVV-lWYz9j3iyD_5NOhwsf9Bu0onIIB8qRIo')))
# print(api_conn.post_championMastery(na1_api.get_champ_mastery_by_summoner_id_and_champ_id('335Zf1OEWrsPVV-lWYz9j3iyD_5NOhwsf9Bu0onIIB8qRIo', '1')))

print(api_conn.post_all_match_data(americas_api.get_match_by_match_id('NA1_4243491999')))