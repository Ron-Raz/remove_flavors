# remove_flavors
Program to remove flavors from list of entries by flavor search pattern

# Installation
This program depends on the Python [Kaltura Native Client Libraries](https://developer.kaltura.com/api-docs/Client_Libraries)
```
pip install KalturaApiClient
```

# Usage
```
python3 remove_flavors <pId> <userId> <adminSecret> <flavorPatternToDelete> <entriesFileName> {ERASE|logOnly}
```
| Parameter        | Description             | Example |
| ---------------- |------------------------ | ------- |
| *pId*              | Your Kaltura Partner ID | 1234567 |
| *userId*           | Your user ID            | ron.raz@kaltura.com |
| *adminSecret*      | Your admin secret from [KMC](https://kmc.kaltura.com/index.php/kmcng/settings/integrationSettings) | *Never share your secret* |
| *flavorPatternToDelete* | Text to match in flavor name | HD/720 |
| *entriesFileName* | Name of text file containing entry IDs, one per line | entries.txt |
| *ERASE* or *logOnly* | *ERASE* actually deletes the matched flavors while *logOnly* just logs the matches without erasing |

# Example
```
$ cat entries.txt
1_4nbc3kuu
1_6kl9795s
1_tetcwunw

$ python3 remove_flavors.py 1234567 ron.raz@kaltura.com e0xxxxx74591xxxxxf4bcdxxxxxb3af7 HD entries.txt logOnly

$ cat remove_flavors.log 
ENTRY_ID     FLAVOR_ID    FLAVOR_NAME                 FLAVOR_SIZE   ACTION
1_tetcwunw   1_5id2ljt9   HD/720 - WEB (H264/2500)    25292         logOnly
1_tetcwunw   1_4nbc3kuu   HD/1080 - WEB (H264/4000)   37785         logOnly

$ python3 remove_flavors.py 1234567 ron.raz@kaltura.com e0xxxxx74591xxxxxf4bcdxxxxxb3af7 HD entries.txt ERASE

$ cat remove_flavors.log 
ENTRY_ID     FLAVOR_ID    FLAVOR_NAME                 FLAVOR_SIZE   ACTION
1_tetcwunw   1_5id2ljt9   HD/720 - WEB (H264/2500)    25292         ERASE
1_tetcwunw   1_4nbc3kuu   HD/1080 - WEB (H264/4000)   37785         ERASE
```
