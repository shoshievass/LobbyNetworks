import requests
import json
import pandas as pd



#function to download a data set
def downloadPartyTimeEvents(outputFile=None, maxi=False, max_val=None, verbose=True):
    dataType='event'
    if maxi:
        print(max_val)
    #url to download from
    next_url="http://politicalpartytime.org/api/v1/"+str(dataType)+"/?offset=0&limit=50&format=json"
    
    #open the file
    if outputFile is None:
        outputFile=dataType+'.json'
    file=open(outputFile, 'w')

    c=0 #counter
    while next_url!=None:
        #possibly end the loop
        if maxi:
            c+=1
            if c>max_val:
                print("auto stop")
                break
        
        #send the request
        r = requests.get(next_url)
        #give few info
        if verbose:
            print(r.url)

        #load as json
        j=json.loads(r.text)
        #dropping meta
        s=j['objects']
        
        #dropping lists & sub items as unreadable
        #if we need more detail, get them from the other datasets, with the id we save
        fields=["beneficiaries", "hosts"]
        for field in fields:
            #loop for each data
            for d in s:
                #id list
                l=[]
                #grabbing only the id
                for b in d[field]:
                    l.append(b['id'])
                #delete and create fields
                del d[field]
                d[field+"_id"]=l
        field="venue"
        #loop for each data
        for d in s:
            if not d[field] is None:
                #delete and create fields
                d[field+"_id"]=d[field]['id']
                del d[field]
            else:
                d[field+"_id"]=None
                del d[field]
                

        
        #writing
        file.write(json.dumps(s))
        file.write('\n')
        
        #possibly end the loop
        if j['meta']['next'] is None:
            break
        #work out the next url
        next_url="http://politicalpartytime.org"+j['meta']['next']

    #close the file
    file.close()
    





#function to download a data set (other then event, which is a bit special)
def downloadPartyTimeData(dataType='venue', outputFile=None, maxi=False, max_val=None, verbose=True):
    if maxi:
        print(max_val)
    #url to download from
    next_url="http://politicalpartytime.org/api/v1/"+str(dataType)+"/?offset=0&limit=50&format=json"
    
    #open the file
    if outputFile is None:
        outputFile=dataType+'.json'
    file=open(outputFile, 'w')

    c=0 #counter
    while next_url!=None:
        #possibly end the loop
        if maxi:
            c+=1
            if c>max_val:
                print("auto stop")
                break
        
        #send the request
        r = requests.get(next_url)
        #give few info
        if verbose:
            print(r.url)

        #load as json
        j=json.loads(r.text)
        #dropping meta
        s=j['objects']
        #writing
        file.write(json.dumps(s))
        file.write('\n')
        
        #possibly end the loop
        if j['meta']['next'] is None:
            break
        #work out the next url
        next_url="http://politicalpartytime.org"+j['meta']['next']

    #close the file
    file.close()




######actual download:

#call the function to download
downloadPartyTimeEvents()
#if not working, try: (it would download only sets of 50 datas, which is muxh quiker, and interesting for fixing bugs)
# downloadPartyTimeEvents(maxi=True, max_val=2)


#if bug, try to call the function as:
# downloadPartyTimeData('venue', maxi=True, max_val=4)
downloadPartyTimeData('venue')
downloadPartyTimeData('lawmaker')
downloadPartyTimeData('host')
