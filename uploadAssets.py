'''
Bulk create and optionally publish Assets - See comments below. (The publish action is commented out when this is written)
Limitation: Only support files, not folders. Does not look for files in nested folders.
oskar.eiriksson@contentstack.com
2021-01-26

--- Update 2024-01-17 ---
mimetypes library does not support webp: https://bugs.python.org/issue38902
Hardcoded webp files to image/webp - although it correctly works on my machine, it might not work on yours.
--- Update 2024-01-17 ---

'''
import os
import cma
import mimetypes

folder = '/tmp/tmpImages/' # Path to folder with all assets that you want to import. Must end with a '/'.
locales = ['en-us'] # An array of languages - Used if you want to publish asset, can publish to more than one.
environments = ['development'] # An array of environments - Used if you want to publish asset, can publish to more than one.
parentFolder = None # UID of parent folder being something like this: 'bltcbf66fcb8b9b3d6a' - Set to None if you want to import to root folder.

'''
Uncomment this (comment other part of code below that while running) to see uids and names of all folders - if you want to define a folder to bulk import to.
'''
# allFolders = cma.getAllFolders()
# for folder in allFolders['assets']:
#     print(folder['uid'], folder['name'])

'''
Bulk create below - Remember to comment out below if you're only running the script to see the folders in your stack.
'''

metaData = {
    'asset': {
        'parent_uid': parentFolder
        }
}

for f in os.listdir(folder):
    if f.endswith('.webp'):
        metaData['asset']['content_type'] = 'image/webp'
    else:
        metaData['asset']['content_type'] = mimetypes.guess_type(f)[0]
    filePath = folder + f
    try:
        newAsset = cma.createAsset(filePath, metaData, f)
    except IsADirectoryError as e:
        print('Skipping folder: ' + f + ' - This script only support files, not folders.')
        continue
    '''
    Publishing Asset below - Comment out if you only want to create it, not publish
    '''
#     if newAsset:
#         uid = newAsset['asset']['uid']
#         cma.publishAsset(uid, locales, environments)

