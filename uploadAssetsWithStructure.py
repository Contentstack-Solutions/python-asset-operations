'''
Bulk create files and folders
vidar.masson@contentstack.com
2023-05-26

--- Update 2024-01-17 ---
mimetypes library does not support webp: https://bugs.python.org/issue38902
Hardcode fix
--- Update 2024-01-17 ---

'''
import os
import cma
import json
import mimetypes

ALLOW_DUPLICATES = False # Set to True if you want to allow duplicate filenames in the same folder. If set to False, the script will not upload files with duplicate filenames.
rootfolder = '/tmp/tmpImages/' # Path to folder with all assets that you want to import. Must end with a '/'.

def pp(obj):
    print(json.dumps(obj, indent=4))

def getMetadata(parentFolderUid, filename):
    if filename.endswith('.webp'):
        mime = 'image/webp'
    else:
        mime = mimetypes.guess_type(filename)[0]
    return {
        'asset':
            {
                'parent_uid': parentFolderUid,
                'content_type': mime
            }
        }


file_list = [] # file_list contains all files paths that should be synced from local filesystem to the stack
folderlookup = {}  # folderlookup contains data on all folders in the stack

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

#pp(path2uid)
#pp(folderlookup)


'''
Start by creating all folders and make a list of files to by synced
'''
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
            parent_path = os.path.dirname(relative)
            newFolder = cma.createFolder(name, path2uid[parent_path] if parent_path in path2uid else None)
            # Update folderlookup base storage
            folderlookup[newFolder['asset']['uid']] = {
                'uid': newFolder['asset']['uid'],
                'parent_uid': newFolder['asset']['parent_uid'],
                'name': newFolder['asset']['name'],
                'path': relative,
            }
            # Update path2uid lookups
            path2uid[relative] = newFolder['asset']['uid']

existing_files = []
if not ALLOW_DUPLICATES:
    all_files = cma.getAllAssets()['assets']
    for item in all_files:
        if not item['is_dir']:
            relpath = folderlookup[item['parent_uid']]['path'] if ('parent_uid' in item and item['parent_uid']) in folderlookup else ''
            fpath = os.path.join(relpath, item['filename'])
            existing_files.append(fpath)

for item in file_list:
    if item in existing_files:
        print('Skipping existing file: ' + item)
        continue
    parent_uid = path2uid[os.path.dirname(item)] if os.path.dirname(item) in path2uid else None
    fname = os.path.basename(item)
    cma.createAsset(rootfolder + item, getMetadata(parent_uid, fname), fname)
    print('Created file: ' + item)
