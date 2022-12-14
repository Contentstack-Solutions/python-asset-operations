'''
Gets assets and downloads them. Either all Assets or only assets from a folder

Limitation: Does not traverse nested folders - You will need to run this script on any folder individually. (See line 26)

2022-12-14
oskar.eiriksson@contentstack.com

'''
import os
import requests
import config
import cma

csFolder = 'blt53574d60024f8472' # Either the folder uid or None. If set to None the code attempts to downloads all the assets from the stack. If you specify a csFolder, it will need to be the uid of the folder you want to fetch from (on the format: bltxxxxx)
localFolder = '/tmp/downloadFolder/' # Where should we download all the assets to? Path must end with a slash ("/"). Folder must exist on local drive before running script.

query = None
if csFolder:
    query = '&query={"parent_uid": "' + csFolder + '"}'

assets = cma.getAllAssets(query)

if assets:
    for asset in assets['assets']:
        if asset['is_dir']:
            config.logging.info('{}Nested folder detected. Name: {} UID: {} - If you need to download assets from this folder you need to run this script again with this UID.{}'.format(config.BOLD, asset['name'], asset['uid'], config.END))
        else:
            filename = asset['filename']
            url = asset['url']
            config.logging.info('Downloading ' + filename)
            r = requests.get(url)
            open(localFolder + filename, 'wb').write(r.content)
            if os.path.exists(localFolder + filename):
                config.logging.info('Asset downloaded to {}{}'.format(localFolder, filename))
            else:
                config.logging.error('Something failed - Please check config.')
