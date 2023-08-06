from plexapi.myplex import MyPlexAccount
import os
import requests

def plexAuth():
    plex_auth_info = {
        "username": os.environ['PLEX_USERNAME'],
        "password": os.environ['PLEX_PASSWORD'],
        "server": os.environ['PLEX_SERVER_NAME']
    }

    account = MyPlexAccount(plex_auth_info['username'], plex_auth_info['password'])
    plex = account.resource(plex_auth_info['server']).connect()
    return plex

def readPlexCollections():
	plex = plexAuth()
	collections = plex.library.sections()
	return collections

def plexUpdate():
	plex = plexAuth()
	update(plex)
	notify("Plex Update Requested.")	
	return 0

def update(plex):
    collections = plex.library.sections()
    task = plex.library.update()
    return task

def notify(message):
	if os.environ.get('PUTIO_NOTIFY') is not None:
		if os.environ.get('PUSHOVER_USER') is None and os.environ.get('PUSHOVER_TOKEN') is None:
			print("[WARN] Ensure PUSHOVER_TOKEN and PUSHOVER_USER are set in environment.")
		else:
			notification_data = "token=%s&user=%s&device=putio-cli&message=%s" % (os.environ['PUSHOVER_TOKEN'], os.environ['PUSHOVER_USER'], message)
			headers = {"Content-type": "application/x-www-form-urlencoded"}
			notification = requests.post("https://api.pushover.net/1/messages.json", headers=headers, data=notification_data)
	return 0

def main():
    plex = plexAuth()
    try:
        scan = update(plex)
        notify("Plex Updated.")
    except Exception as e:
        scan = e
    return scan