import asyncio
import datetime
import pytz, dateutil.parser
import requests
import json
import threading
from merakitools import lib

class NetworkEvents(threading.Thread):
	def __init__(self, org_id,networks):
		"""
		Init Function or Validateorginization
		Args:
			org_id(string): Orginization ID from Meraki
		"""
		threading.Thread.__init__(self)
		self.org_id = org_id
		self.networks = networks
	
	def run(self):
		"""
		Start the ASYNC fun fuctions and waits for completions to restore
		Cache
		Returns:

		"""
		asyncio.run(self._async_run())
	
	async def _async_run(self):
		"""
		Async version of the run function loops through all networks
		then sends the network to the valate proccessor
		Returns:

		"""
		print(
				f'\tOrgName: {self.org_id}Thread PID:{threading.currentThread().native_id}'
		)
		count = 0
		time_fmt = '%H:%M:%S'
		date_fmt = '%m/%d/%Y'
		full_fmt = '%Y-%m-%dT%H:%M:%S%z'
		date_start = "2021-09-29T00:00:00Z"
		date_stop = dateutil.parser.parse('2021-09-30T00:00:00Z')
		meta = json.dumps({"index": {}})
		headers = {
				'Authorization': 'Basic am9zaDpDb3JlZnVja2VkbWUxIQ==',
				'Content-Type' : 'application/json'
		}
		url = f"https://es.ciscolabnet.com/doe-meraki-wireless/_bulk"
		with lib.MerakiAsyncApi() as sdk:
			for network in self.networks:
				try:
					events = await sdk.networks.getNetworkEvents(
						networkId=network['id'], startingAfter=date_start,
						includedEventTypes=["wpa_auth", "association"],
						perPage=1000)
					event_list = events['events']
					pageEnd = dateutil.parser.parse(events['pageEndAt'])
					pageEnd = pageEnd + datetime.timedelta(0, 1)
					timeDiff = pageEnd > date_stop
					pageEnd = pageEnd.strftime(full_fmt)
				except Exception as e:
					print(f"Network {network['name']} - End time: {pageEnd} Error with get events {str(e)}")
					
				
				while not timeDiff:
					try:
						events = await sdk.networks.getNetworkEvents(
								networkId=network['id'],
								startingAfter=pageEnd,
								includedEventTypes=["wpa_auth",
								                    "association", ],
								perPage=1000)
						print(
							f"Network: {network['name']} - Page Start Time: {events['pageStartAt']} Page End Time: {events['pageEndAt']}")
						event_list.extend(events['events'])
						pageEnd = dateutil.parser.parse(events['pageEndAt'])
						timeDiff = pageEnd > date_stop
						pageEnd = pageEnd + datetime.timedelta(0, 1)
						pageEnd = pageEnd.strftime(full_fmt)
					except Exception as e:
						print(f"Network {network['name']} - End time: {pageEnd} Error with get events {str(e)}")
				payload = ""
				print(
					f'Building Payload for Network: {network["name"]} Event list size: {len(event_list)}')
				for event in event_list:
					# print(event)
					try:
						utctime = dateutil.parser.parse(event['occurredAt'])
						localtime = utctime.astimezone(
							pytz.timezone('US/Eastern'))
						# print(f"{localtime.strftime(date_fmt)}-{localtime.strftime(time_fmt)}:{event['clientId']}-{event['clientDescription']} Connected to {network['name']} - {event['ssidName']} " )
						count = count + 1
						# id = random.random()+count
						
						event.pop("occurredAt")
						event["timeStamp"] = localtime.strftime(full_fmt)
						event["networkName"] = network["name"]
						data = json.dumps(event)
						payload += f"{meta}\n{data}\n"
					except Exception as e:
						print(f"Error Building payload for Network: {network['name']} Error: {str(e)}")
				
				if len(payload) > 0:
					print(f'Network: {network["name"]} - Payload Size: {len(event_list)}')
					try:
						response = requests.request("POST", url,
						                            headers=headers,
						                            data=payload)
						print(f'Network: {network["name"]} fished eith response code" {response.status_code}')
					except Exception as e:
						print(
							f"Error uploading to Elsstic Search for: {network['name']} Error: {str(e)}")