# python-asset-operations
* Create/Upload Assets - `uploadAsset.py`
* Replace Asset - `replaceAsset.py` (Similar function to change data around the asset - this one replaces file and filename)
* Get and Download Asset - `getAsset.py`
* Get and download all assets (or from a specified folder) - `downloadMultipleAssets.py`

*NOT OFFICIALLY SUPPORTED BY CONTENTSTACK*

## Prerequisites:
* Contentstack Account.
* Install Python 3 (Developed using Python 3.9.1 on Macbook).
* Install Python package:
  * `pip install requests`

## Define environmental variables
e.g. `variables.env` file:
```
CS_REGION=NA (Either NA or EU)
CS_APIKEY=blt972.....
CS_MANAGEMENTOKEN=cs....

export CS_REGION CS_APIKEY CS_MANAGEMENTOKEN
```
and run `source variables.env` in the terminal.

