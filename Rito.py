# Ben Closner
# 4/10/15
# Rito uses the Riot API to find when account names will become available.
# (API keys are technically private)
#
# still WIP
#
# example:
#
# a = Rito.api('My Riot API key here')
# a.text_output('summoner name in question')
# 


import urllib.request
import json
import datetime


MY_KEY = 'ce14c093-38d2-4a49-acf4-2a5a6e8f4d7e'  #just used for testing
MY_SUMMONER_ID = 22788951 			 #just used for testing
BASE_URL = r'https://na.api.pvp.net/'




class api:
    	
	def __init__(self, api_key = MY_KEY, region = 'na'):
		self.api_key = r'?api_key=' + api_key										
		self.region = region											

	def _summoner_id_from_name(self, name):	
		formatted_name = name.replace(' ', r'%20')							                              		#replaces the spaces in the name with needed symbols 
		summoner_id_api = r'api/lol/{region}/v1.4/summoner/by-name/{summonerNames}'			      		#this is the part of the API that contains basic summoner info
		url = (BASE_URL + summoner_id_api + self.api_key).format(region = self.region, summonerNames = formatted_name)	#the url is combined
		
		try:														#if a name has never been created, the api throws a 404
			data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))					#the api is called, the data is read, the bytestring is converted into a string, the string is made into a dict (probably not the best way to do this)
			return data[name.replace(' ', '').lower()]								#all of the data is returned. This dict contains the important summoner id, summoner name, and  summoner level
		except urllib.error.HTTPError:
			return None
		
		
	
	def _most_recent_game(self, summoner_id):
		last_ten_api = r'api/lol/{region}/v1.3/game/by-summoner/{summonerId}/recent'                                  #this is the part of the API which containts match history
		url = (BASE_URL + last_ten_api + self.api_key).format(region = self.region, summonerId = summoner_id)         #this combines the parts of the URL to be called
		data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))					      #the api is called, the data is read, the bytestring is converted into a string, the string is made into a dict (probably not the best way to do this)
		epoch = data['games'][0]['createDate']								   	      #the most recent game is picked out, and the date of the most recent game is put into epoc		
		del data												      
		return datetime.datetime.fromtimestamp(int(epoch/1000))						              #takes the epoch value in miliseconds, converts to seconds, and is structured into a years, month week... format
															      #the date returned is in UTC
	def text_output(self, name):
		if any(not x.isalnum() for x in name) or len(name) == 1:							#filters out names with characters not alphanumeric
			print(str(name) + " is not a valid name")
			return
		summoner_info = self._summoner_id_from_name(name)
		if not summoner_info:												#filteres out names never created before
			print("The name " + str(name) + " is not in use")
			return
		latest_game_date = self._most_recent_game(summoner_info['id'])
		account_expires_date_offset = 6 if summoner_info['summonerLevel'] < 7 else summoner_info['summonerLevel']
		account_expires_date = latest_game_date.replace(month = (latest_game_date.month + account_expires_date_offset) % 12, year = latest_game_date.year + (latest_game_date.month + account_expires_date_offset)//12)
		if account_expires_date < datetime.datetime.utcnow():
			print(str(summoner_info['name']) + " is available or unuseable")					#filters any name that has been created and is available now
			return
		
		print(str(summoner_info['name']) + " (lvl " + str(summoner_info['summonerLevel']) + ")", end = '')
		print(" expires on " + account_expires_date.strftime('%m/%d/%y'))						#prints when the name will be availalbe
		#print(" The current time in UTC is " + str(datetime.datetime.utcnow()))
		#print(" This summoners most recent game was on (UTC) " + str(latest_game_date))
		return




def main():
	a = api(MY_KEY)
	a.text_output('javafreak')
	a.text_output('...')
	a.text_output('abc')
	

if __name__ == '__main__':
	main()
