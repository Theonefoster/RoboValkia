import requests
from credentials import robovalkia_client_id, valkia_subscriber_token, valk_channel_id, g_browser_key

def get_subscribers():
	base_url = "https://api.twitch.tv/helix/subscriptions?broadcaster_id={channel_ID}"
	page_url = "https://api.twitch.tv/helix/subscriptions?broadcaster_id={channel_ID}&after={pagination}"
	header = {"Client-ID": robovalkia_client_id, "Authorization": "Bearer " + valkia_subscriber_token}

	all_subscribers = []

	response = requests.get(base_url.format(channel_ID=valk_channel_id), headers=header).json()

	data = response["data"]
	pagination_key = response["pagination"]["cursor"]

	all_subscribers += data

	while data != []:
		response = requests.get(page_url.format(channel_ID=valk_channel_id, pagination=pagination_key), headers=header).json()
		data = response["data"]
		pagination_key = response["pagination"]["cursor"]
		all_subscribers += data

	"""
	Each sub looks like:
	        {
            "broadcaster_id": "3481156",
            "broadcaster_name": "Valkia",
            "gifter_id": "",
            "gifter_name": "",
            "is_gift": false,
            "plan_name": "Valkians! ",
            "tier": "1000",
            "user_id": "12345678",
            "user_name": "TwitchUser123"
        },
	"""

	sub_dict = dict()

	for sub in all_subscribers:
		username = sub["user_name"].lower()
		del sub["user_name"] #makes the file/dict much smaller and I never use this :)
		del sub["broadcaster_id"]
		del sub["broadcaster_name"]
		del sub["gifter_id"]
		del sub["plan_name"]
		sub_dict[username] = sub

	return sub_dict

def get_youtube_sub_count(username):
	url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={username}&key={key}".format(key=g_browser_key, username=username)
	response = requests.get(url).json()
	items = response["items"][0]
	snippet = items["statistics"]
	return snippet["subscriberCount"]

if __name__ == "__main__":
	from time import time 
	print("Getting Subscribers..")
	t = time()
	get_subscribers()
	diff = time() - t
	print("Done in {s} seconds".format(s=round(diff, 2)))
	input()
