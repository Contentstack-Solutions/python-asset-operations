'''
Gets a single asset and saves to file on local drive
2021-01-26
oskar.eiriksson@contentstack.com
'''
import requests
import cma

assetUid = 'blt631e3cc398c2ff73' # Uid of asset to fetch and save
folder = '' # Empty for same folder as code - Will save the file to here. Ends with slash if not empty.

asset = cma.getSingleAsset(assetUid)

print(asset)

url = asset['asset']['url']
filename = asset['asset']['filename']

r = requests.get(url)
open(folder + filename, 'wb').write(r.content)
