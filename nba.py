from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile
from nba_api.stats.static import players
import pandas

playerName = 'Lebron James'
seasonYear = '2015-16'
statCategory = 'GROUP_VALUE'
playerId = players.find_players_by_full_name(playerName)[0]['id']
print(playerId)


player_info = commonplayerinfo.CommonPlayerInfo(player_id= playerId)
playerInfo = player_info.common_player_info.get_data_frame()
# print (avaliableSeasonDF.at[0, 'SEASON_ID'])
print (playerInfo)
# team_id =


seasonInfo = playerfantasyprofile.PlayerFantasyProfile(player_id = playerId, season=seasonYear)

seasonInfoByGame= seasonInfo.opponent.get_data_frame()
print(seasonInfoByGame)
statDF = seasonInfoByGame.loc[:,statCategory]
print(statDF)
