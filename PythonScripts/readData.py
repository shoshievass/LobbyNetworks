import json
import pandas as pd




#function that open the file and create a "good" dataset
def createDataFrame(file):
    ##lists of 50 data are loaded and then merged
    #create list of dataframes and open file
    dataframes=[]
    file=open(file, 'r')
    
    #counter is important for the index
    c=0
    while True:
        #each line is 50 data (as limit=50 when downloading)
        txt=file.readline()
        #possibly stop
        if txt=='':
            break

        #load the data with right index
        j=json.loads(txt)
        l=len(j)
        dataframes.append(pd.DataFrame(j, index=list(range(c, c+l))))
        
        c+=l
    #merge all datasets and return result
    return pd.concat(dataframes)



#actually create the DataFrames
# and print them to get an idea of how they look like...
dfVenue=createDataFrame('venue.json')
print(dfVenue)

dfHost=createDataFrame('host.json')
print(dfHost)

dfLawmaker=createDataFrame('lawmaker.json')
print(dfLawmaker)

dfEvent=createDataFrame('event.json')
print(dfEvent)






