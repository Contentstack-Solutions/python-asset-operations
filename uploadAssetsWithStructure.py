'''
Bulk create files and folders
vidar.masson@contentstack.com
2023-05-25
'''
import os
import cma
import json
import mimetypes

rootfolder = '/tmp/tmpImages/' # Path to folder with all assets that you want to import. Must end with a '/'.
parentFolder = None # UID of parent folder being something like this: 'bltcbf66fcb8b9b3d6a' - Set to None if you want to import to root folder.

def pp(obj):
    print(json.dumps(obj, indent=4))

def getMetadata(parentFolderUid, filename):
    return {
        'asset':
            {
                'parent_uid': parentFolderUid,
                'content_type': mimetypes.guess_type(filename)[0]
            }
        }


file_list = []
folderlookup = {}

all_folders = cma.getAllFolders()['assets']
for folder in all_folders:
    folderlookup[folder['uid']] = {
        'uid': folder['uid'],
        'parent_uid': folder['parent_uid'],
        'name': folder['name']
        }

path2uid = {}

# One pass to add path key to all folders
for folder in folderlookup.keys():
    path = []
    parent = folderlookup[folder]['parent_uid']
    while parent:
        path.append(folderlookup[parent]['name'])
        parent = folderlookup[parent]['parent_uid']
    path.reverse()
    path.append(folderlookup[folder]['name'])
    folderlookup[folder]['path'] = '/'.join(path)
    path2uid[folderlookup[folder]['path']] = folderlookup[folder]['uid']

pp(path2uid)
pp(folderlookup)

for root, dirs, files in os.walk(rootfolder):
    for name in files:
        full = os.path.join(root, name)
        relative = os.path.relpath(full, rootfolder)
        file_list.append(relative)
    for name in dirs:
        full = os.path.join(root, name)
        # get relative path
        relative = os.path.relpath(full, rootfolder)
        if relative not in path2uid:
            # create folder
            print('Creating folder: ' + relative)
            parent = os.path.dirname(relative)
            newFolder = cma.createFolder(name, )
            folderlookup[newFolder['folder']['uid']] = {
                'uid': newFolder['folder']['uid'],
                'parent_uid': newFolder['folder']['parent_uid'],
                'name': newFolder['folder']['name'],
                'path': relative,
            }
            
        