import json
import sys
import tabulate

file1 = sys.argv[1]
file2 = sys.argv[2]

        
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def processFile(file):
    with open(file,'r') as fileData:
        fileString = fileData.read()
        fileDictionary = json.loads(fileString)
        return flatten_json(fileDictionary)


def compareKeys(dict1, dict2):
    keyTup = ([],[],[])
    for k1 in dict1:
        if k1 in dict2:
            keyTup[0].append(k1)
            continue
        keyTup[1].append(k1)
    
    for k2 in dict2:
        if k2 not in dict1:
            keyTup[2].append(k2)

    return keyTup


def printUniqueKeys(uniqueKeys):
    if len(uniqueKeys[0]) == 0 & len(uniqueKeys[1]) == 0:
        print('\n%s and %s have identical keys!' %(file1,file2))
        return
    print("\nTable of unique keys:\n")
    rows = max(len(uniqueKeys[0]),len(uniqueKeys[1]))
    keyList = []

    for i in range(0,rows):
        emptyArr = [None]*2

        try:
            emptyArr[0] = uniqueKeys[0][i]
        except IndexError:
            emptyArr[0] = ""

        try:
            emptyArr[1] = uniqueKeys[1][i]
        except IndexError:
            emptyArr[1] = ""
        
        keyList.append(emptyArr)

    print(tabulate.tabulate(keyList,headers=[file1,file2],tablefmt="presto"))
        

def compareValues(dict1, dict2, sharedKeys):
    if len(sharedKeys) == 0:
        print("%s and %s have no common keys" %(file1,file2))
        return 
       
    print("\nTable of inconsistent key value pairs:\n")
    keyList = []
    for key in sharedKeys:
        if dict1[key] != dict2[key]:
            tempList = []
            tempList.append(key)
            tempList.append(dict1[key])
            tempList.append(dict2[key])
            keyList.append(tempList)
    
    print(tabulate.tabulate(keyList, headers=["key",file1,file2],tablefmt="fancy_grid"))
    


dict1 = processFile(file1)
dict2 = processFile(file2)
keys = compareKeys(dict1,dict2)
uniqueKeys = [keys[1],keys[2]]
printUniqueKeys(uniqueKeys)
compareValues(dict1,dict2,keys[0])
            
             











    





    



