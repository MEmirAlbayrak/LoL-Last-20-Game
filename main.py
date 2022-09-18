from riotwatcher import LolWatcher, ApiError
import pandas as pd
import json


# golbal variables
api_key = 'YOUR API KEY'
watcher = LolWatcher(api_key)
my_region = 'Region (tr1, eu1 exc.)'
player = 'PLAYER NAME'
#-----------------------
me = watcher.summoner.by_name(my_region, player)

my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])
file = open('data.txt', 'w') 
file.write(player + "Stats" + "\n")
file.close()

for i in range(20):
    # fetch last match detail
    last_match = my_matches['matches'][i]
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])

    participants = []
    for row in match_detail['participants']:
        participants_row = {}
        participants_row['champion'] = row['championId']
        participants_row['win'] = row['stats']['win']
        participants_row['kills'] = row['stats']['kills']
        participants_row['deaths'] = row['stats']['deaths']
        participants_row['assists'] = row['stats']['assists']
        participants_row['champLevel'] = row['stats']['champLevel']
        participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
        participants.append(participants_row)
    df = pd.DataFrame(participants)

    # check league's latest version
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
    # Lets get some champions static information
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    # champ static list data to dict for looking up
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    for row in participants:
        row['championName'] = champ_dict[str(row['champion'])]

    # print dataframe
    df = pd.DataFrame(participants)
    
    file = open('data.txt', 'a') 
    file.write(str(df)) 
    file.write("\n")
    file.write("----------------------------------------------\n")


file.close()