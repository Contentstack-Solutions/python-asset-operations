'''
Update Assets
oskar.eiriksson@contentstack.com
2021-01-26
'''
import mimetypes
import cma

assetUid = 'bltd367135c3ebffe40' # Asset UID in Contentstack that you want to replace with a new file
filepath = '/Users/oskar/Downloads/ContentStackTest.txt' # Full path to file on local drive - that you want to use to replace in Contentstack with
filename = filepath.split('/')[-1]

metaData = {
    'asset': {
        #'parent_uid': '',
        'content_type': mimetypes.guess_type(filepath)[0]
        }
} 

replacedAsset = cma.replaceAsset(assetUid, filepath, metaData, filename)



