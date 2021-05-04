# Created by Stevan Gavrilovic, NHERI SimCenter, University of California, Berkeley

import requests
import json
import os
import sys
import hashlib
import zipfile
import stat

from pathlib import Path

#baseURL = 'https://sandbox.zenodo.org/api/'
baseURL = 'https://zenodo.org/api/'

from zipfunctions import *

def deleteIfExists(deposition_id, ACCESS_TOKEN):
   
    print("In delete files")
    print("Root deposition id " + str(deposition_id))
    
    r = requests.get(baseURL + 'deposit/depositions', params={'q' : deposition_id, 'access_token': ACCESS_TOKEN})
    
    if r.status_code != 200:
        print(r.status_code)
        print(r.json())
        print("Error getting in deleteIfExists")
        sys.exit(-1)
           
    if "latest_draft" not in r.json()[0]["links"]:
        return 1
    
    newVer = r.json()[0]["links"]["latest_draft"]
        
    r = requests.get(newVer,params={'access_token': ACCESS_TOKEN})
        
    if r.status_code != 200:
        print(r.status_code)
        print(r.json())
        print("Error getting latest version in deleteIfExists")
        sys.exit(-1)
        
    newVerJson = r.json()
    
    # print(newVerJson)
    
    verID = newVerJson["id"]
    
    print("Deleting draft version " + str(verID))
    
    r = requests.delete(baseURL + 'deposit/depositions/' + str(verID),
                    params={'access_token': ACCESS_TOKEN})
        
    # Return 0 if successful
    if r.status_code == 204 or r.status_code == 201:
        return 0
        
    print(r.status_code)
    print(r.json())
    print("Error deleting draft version in deleteIfExists")
    sys.exit(-1)
        
    return 1
    

# Get the current path
currPath = os.getcwd()

# Get the path two directories up from the current path
pathFiles = Path(currPath).parents[1]

filelist = []
pathList = []

# Create the zip files
for dir in next(os.walk(pathFiles))[1] :
    # Skip the folder if it is a git folder
    if '.git' in dir :
        continue
    
    folder = os.path.join(pathFiles,dir)
    
    output_path = str(pathFiles)+"/"+str(dir)+".zip"

    with zipfile.ZipFile(output_path, "w") as zip_file:
        for path in next(os.walk(folder)) :
        # Skip the folder if it is a git folder
            if '.git' in path :
                continue
                
            if os.path.isdir(str(path)):
                add_directory(zip_file, path, os.path.basename(path))
            elif os.path.isfile(str(path)):
                add_file(zip_file, path, os.path.basename(path))

    # Checksum should be deteriminstic between runs given that no files have changed
    checksum = hashlib.md5(open(output_path,'rb').read()).hexdigest()
    print(checksum)
  
print("Done zipping")

# Find all files with a .zip extension
for root, dirs, files in os.walk(pathFiles):
    for file in files:
            if file.endswith(".zip"):
                #append the file name and path to the lists
                pathList.append(os.path.join(root,file))
                filelist.append(file)

# Print the name of each file
for name in filelist:
    print(name)
    
# Print the path to each file
for name in pathList:
    print(name)

# Get the access token called ZENODO_KEY that is stored in github secrets
ACCESS_TOKEN = os.environ['ZENODO_KEY']

# Create the standard headers
headers = {"Content-Type": "application/json"}

params = {'access_token': ACCESS_TOKEN}

#print(r.status_code)
#print(r.json())

# The target URL is a combination of the bucket link with the desired filename
# seperated by a slash.

for ii in range(0, len(filelist)):

    filename = filelist[ii]
    path = pathList[ii]
    
    print("File Name:"+filename)
    
    base=os.path.basename(path)
    os.path.splitext(base)
    nameNoExt = os.path.splitext(base)[0]

    # The metadata
    data = {
            'metadata': {
            'title': 'R2D Tool Example ' + nameNoExt,
            'upload_type': 'dataset',
            'description': 'R2D Tool Example ' + nameNoExt,
            'creators': [{'name': 'Gavrilovic, Stevan',
            'affiliation': 'NHERI SimCenter, UC Berkeley'}]
                        }
            }

    r = requests.get(baseURL + 'deposit/depositions',
                  params={'q' : filename, 'sort' : 'mostrecent', 'access_token' : ACCESS_TOKEN})
                  
    if r.status_code != 200:
        print(r.status_code)
        print(r.json())
        print("Error posting request")
        sys.exit(-1)

    # First check if the file is available. If it is, then update. If not, then post a file new

    jsonObj = r.json()
    
    found = False

    if len(jsonObj) != 0 :
        found = True
        
        #print(jsonObj)
    
        # The root ID, i.e., of the very first submission
        rootID = jsonObj[0]['conceptrecid']
        
        # Delete an incomplete draft if one exists
        # This occurs if an existing upload fails due to bad network connection
        res = deleteIfExists(rootID, ACCESS_TOKEN)
        
        # If an incomplete submission was deleted, get the id to the newest deposition
        if res == 0 :
            r = requests.get(baseURL + 'deposit/depositions', params={'q' : filename, 'sort' : 'mostrecent', 'access_token' : ACCESS_TOKEN})
                  
            if r.status_code != 200:
                print(r.status_code)
                print("Error posting request")
                sys.exit(-1)
                            
    if found == False :
        print('Uploading new file version of: ' + filename)
            
        r = requests.post(baseURL + 'deposit/depositions',
                        params=params,
                        json={},
                        # Headers are not necessary here since "requests" automatically
                        # adds "Content-Type: application/json", because we're using
                        # the "json=" keyword argument
                        # headers=headers,
                        headers=headers)
                        
        if r.status_code != 201:
            print(r.status_code)
            print(r.json())
            print("Error posting request")
            sys.exit(-1)

        bucket_url = r.json()["links"]["bucket"]
        deposition_id = r.json()['id']

        with open(path, "rb") as fp:
            r = requests.put(
                "%s/%s" % (bucket_url, filename),
                data=fp,
                params=params,
            )
            if r.status_code != 200:
                print(r.status_code)
                print(r.json())
                print("Error put file data")
                sys.exit(-1)
        
        url = baseURL + 'deposit/depositions/%s' % deposition_id
        r = requests.put(url,
            params={'access_token': ACCESS_TOKEN}, data=json.dumps(data),
            headers=headers)
        
        if r.status_code != 200:
            print(r.status_code)
            print(r.json())
            print("Error in put metadata")
            sys.exit(-1)

        # Publish it on Zenodo
        r = requests.post(baseURL + 'deposit/depositions/%s/actions/publish' % deposition_id, params={'access_token': ACCESS_TOKEN} )

        print("Published first version of " + filename + "successfully")

        if r.status_code != 202:
            print(r.status_code)
            print(r.json())
            print("Error publishing first version")
            sys.exit(-1)

    else:
        print('Updating file: ' + filename)
        
        latestObj = jsonObj[0]
        
        deposition_id = latestObj['id']
        
        print('Deposition ID original: ' + str(deposition_id))

        # Get the checksum of the zip file in the cloud - in this case there is only one: the zip file
        checksum = latestObj["files"][0]["checksum"]
        
        # Get the checksum of the zip file locally
        checksumLocal = hashlib.md5(open(path,'rb').read()).hexdigest()
        
        # Do not update if the files are the same
        if checksum == checksumLocal :
            print('Checksums for deposition ID: ' + str(deposition_id) + ' match, skipping')
            continue
      
        # If the file is updated, i.e., something has changed, create the new version
        url = baseURL + 'deposit/depositions/'+str(deposition_id)+'/actions/newversion'
        r = requests.post(url, params={'access_token': ACCESS_TOKEN})
        
        if r.status_code != 201:
            print(r.status_code)
            print(r.json())
            print("Error posting updated version")
            sys.exit(-1)
        
        newVer = r.json()["links"]["latest_draft"]
        
        r = requests.get(newVer,params={'access_token': ACCESS_TOKEN})
        
        if r.status_code != 200:
            print(r.status_code)
            print(r.json())
            print("Error getting latest version")
            sys.exit(-1)
        
        newVerJson = r.json()
        
        # print(newVerJson)
        
        bucket_url = newVerJson["links"]["bucket"]
        print("The bucket url:" + bucket_url)

        deposition_id = newVerJson['id']
        
        print('Deposition ID new: ' + str(deposition_id))
                
        with open(path, "rb") as fp:
            r = requests.put(
                "%s/%s" % (bucket_url, filename),
                data=fp,
                params={'access_token': ACCESS_TOKEN},
            )
            if r.status_code != 200:
                print(r.status_code)
                print(r.json())
                print("Error put file data")
                sys.exit(-1)
        
        # Publish it on Zenodo
        r = requests.post(baseURL + 'deposit/depositions/%s/actions/publish' % deposition_id,
        params={'access_token': ACCESS_TOKEN} )

        print("Published update of " + filename + " successfully")
 
        if r.status_code != 202:
            print(r.status_code)
            print(r.json())
            print("Error publishing new version")
            sys.exit(-1)
    
