from collections import namedtuple 
from datetime import datetime
from datetime import date 
import subprocess
import shlex
import re

# chocoPackage = namedtuple('chocoPackage',[
#     'version',
#     'publishDate',
#     'approvalDate',
#     'age'
# ])

# ------------------------------------------------------ 
#  Get the output from chocolatey/Powershell
# ------------------------------------------------------ 
# packageName = 'Tableau-Desktop'
# commandList = shlex.split(f'choco search {packageName} --all --verbose')
# process = subprocess.Popen(commandList,stdout=subprocess.PIPE)
# output = process.communicate()[0].decode("utf-8")

# if you want to get the output from a file, read this
# with open('test.txt','r',encoding='utf-16') as chocoOutput:
#     output = chocoOutput.read()



def checkInstalledApps(packageID):
    commandList = shlex.split(f'choco search {packageID} --all --local-only')
    # commandList = shlex.split(f'choco search {packageID} --all --verbose')
    process = subprocess.Popen(commandList,stdout=subprocess.PIPE)
    output = process.communicate()[0].decode("latin-1")
    print(output)

def checkChocoPackages(packageID):
    commandList = shlex.split(f'choco search {packageID} --all --verbose')
    process = subprocess.Popen(commandList,stdout=subprocess.PIPE)
    output = process.communicate()[0].decode('latin-1')

    appPackages =[]
    # for eachPackageString in output.split("\n\n"):
    for eachPackageString in output.split("\r\n\r\n"):
        correctedPackageID = 'sql-server-management-studio' if packageID == 'ssms' else packageID
        regexSearchResult = re.search(f'^{correctedPackageID}.*',eachPackageString,re.DOTALL)    
        if regexSearchResult:
            appPackages.append(regexSearchResult.group())

    for eachPackage in appPackages:
        version = re.search(f'(?<={correctedPackageID} )(\d+\.|\d+ )+',eachPackage)
        if version:
            version = version.group().strip()
        
        publishDate =  re.search('(?<=Published: )\d{1,2}/\d{2}/\d{4}',eachPackage)
        if publishDate:
            publishDateString = publishDate.group() 
            publishDate = datetime.strptime(publishDateString,'%d/%m/%Y')
            age = (datetime.today() - publishDate).days
        
        # approvalDate = re.search('(?<=Package approved as a trusted package on )[a-zA-z]{3} \d{2} \d{4}',eachPackage)
        approvalDate = re.search('(?<=Package approved)(.*)([a-zA-z]{3} \d{2} \d{4})',eachPackage)
        if approvalDate:
            approvalDate = approvalDate.group(2)
        
        
        print(version,publishDateString,approvalDate,age)

if __name__ == "__main__":
    print("=========================")
    print("installed choco packages")
    print("=========================")

    checkInstalledApps('Tableau-Desktop')
    # checkInstalledApps('R.Studio')

    print("=========================")
    print("available choco packages")
    print("=========================")

    checkChocoPackages('Tableau-Desktop')
    # checkChocoPackages('R.Studio')
