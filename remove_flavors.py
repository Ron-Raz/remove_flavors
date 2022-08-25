import re
import sys
from KalturaClient import *
from KalturaClient.Plugins.Core import *

#
# This program removes flavors from a list of entries provided as input.
# 
# Input:
#       Commandline parameters: <pId> <userId> <adminSecret> <flavorPatternToDelete> <entriesFileName> {ERASE|logOnly}
#       Text files that includes list of entries for processing, an entry ID per line
# 
# Logic:
#       1. Program uses the Kaltura API to iterate through the list of entries
#       2. for each entry, it will ge the list of flavors, and look for a match with the flavor pattern from the configuration
#       3. if there are any matches, they will be deleted
#       4. output a log for each entry: entry ID, found/not found, flavor found/not found, if found, whether deleted successfully, size of flavor
# 

myConfig = {
    'pId': None,
    'adminSecret': None, 
    'userId': None,
    'flavorPatternToDelete': None,
    'entriesFileName': None,
    'logFileName':'remove_flavors.log',
    'action': None }

myFiles= {
    'in': None,
    'out': None }

myKaltura= {
    'serviceUrl': 'https://www.kaltura.com/',
    'client': None ,
    'filterAsset': None,
    'pagerAsset': None}

myFlavorMap= {}

exceptions = { 
    'usage': 'Use following commandline arguments: <pId> <userId> <adminSecret> <flavorPatternToDelete> <entriesFileName> {ERASE|logOnly}',
    'io': 'Error when opening in/out files. Check permissions etc.' }

def processConfig():
    try:
        myConfig['pId']= int(sys.argv[1])
        myConfig['userId']= sys.argv[2]
        myConfig['adminSecret']= sys.argv[3]
        myConfig['flavorPatternToDelete']= re.compile(re.escape(sys.argv[4]))
        myConfig['entriesFileName']= sys.argv[5]
        myConfig['action']= sys.argv[6]
        print('myConfig=',myConfig)
    except:
        raise ValueError(exceptions['usage'])

def openFiles():
    try:
        myFiles['in']= open(myConfig['entriesFileName'],'r')
        myFiles['out']= open(myConfig['logFileName'],'w')
        myFiles['out'].write('\t'.join(['ENTRY_ID', 'FLAVOR_ID', 'FLAVOR_NAME','FLAVOR_SIZE', 'ACTION'])+'\n')
    except:
        raise ValueError[exceptions['io']]

def closeFiles():
    for file in myFiles:
        myFiles[file].close()

def kalturaInit():
    config = KalturaConfiguration()
    config.serviceUrl = myKaltura['serviceUrl']
    myKaltura['client'] = KalturaClient(config)
    ks =  myKaltura['client'].session.start(
        myConfig['adminSecret'],
        myConfig['userId'],
        KalturaSessionType.ADMIN,
        myConfig['pId'])
    myKaltura['client'].setKs(ks)
    myKaltura['filterAsset']= KalturaAssetFilter()
    myKaltura['filterAsset'].sizeGreaterThanOrEqual = 1
    myKaltura['pagerAsset']= KalturaFilterPager()

def kalturaGetFlavorMap():
    filter = KalturaFlavorParamsFilter()
    pager = KalturaFilterPager()
    result = myKaltura['client'].flavorParams.list(filter, pager)
    for flavor in result.getObjects():
        myFlavorMap[flavor.id]= flavor.name

def kalturaProcessFlavor(flavor):
    myFiles['out'].write('\t'.join([flavor.entryId, flavor.id, myFlavorMap[flavor.flavorParamsId], str(flavor.size), myConfig['action']])+'\n')
    if myConfig['action'] == 'ERASE':
        result = myKaltura['client'].flavorAsset.delete(flavor.id)
    
def kalturaProcessEntryId(entryId):
    myKaltura['filterAsset'].entryIdEqual = entryId
    result = myKaltura['client'].flavorAsset.list(myKaltura['filterAsset'], myKaltura['pagerAsset'])
    for flavor in result.getObjects():
        if myConfig['flavorPatternToDelete'].match(myFlavorMap[flavor.flavorParamsId]):
            kalturaProcessFlavor(flavor)

def main():
    
    processConfig()
    openFiles()
    kalturaInit()
    kalturaGetFlavorMap()

    try:
        while True:
            entryId= myFiles['in'].readline().strip()
            if not entryId:
                break
            kalturaProcessEntryId(entryId)
    except:
        raise ValueError(exceptions['usage'])

    closeFiles()
    
main()
