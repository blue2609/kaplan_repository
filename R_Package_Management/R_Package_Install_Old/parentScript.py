import re
import os
import subprocess
from pprint import pprint

# the function which will allow us to execute the R Script
def rscript(requiredPackages):
    r_path = 'C:/Program Files/R/R-3.6.1/bin/Rscript'
    r_script = 'R Package Install.r'
    commands = [r_path,r_script]
    return subprocess.call(commands + requiredPackages)

# Create data structure which will keep track of things
requiredPackages = []
fileLibDict = dict() 

folderPath = './R Scripts'
for fileName in os.listdir(folderPath):

    RFileName = re.search('.*\.r$',fileName,re.IGNORECASE)

    if RFileName:
        RFileName = RFileName.group()
        fileLibDict[RFileName] = []
        RFilePath = f'{folderPath}/{RFileName}'

        with open(RFilePath,'r') as RFile:
            line = RFile.readline()
            while line != '': # The EOF char is an empty string
                packageName = re.search('(?<=library\().+(?=\))',line)
                
                # if packageName is not NULL
                if packageName:
                    packageName = packageName.group()
                    
                    # if there's more than one argument passed to 
                    # the library() function, take the first element
                    argsList = packageName.split(',')
                    if len(argsList)> 1:
                        packageName = argsList[0] 
                    packageName = packageName.strip('\"\'')
                    fileLibDict[RFileName].append(packageName)

                line = RFile.readline()
 

pprint(fileLibDict)
([requiredPackages.extend(listOfPackages) for listOfPackages in fileLibDict.values()])
pprint(sorted(set(requiredPackages)))
output = rscript(requiredPackages)
print(output)
