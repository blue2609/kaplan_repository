import shlex
import subprocess 
import os

packageName = 'Tableau-Desktop'
activationKey = os.environ.get('TABLEAU_ACTIVATION_KEY')
version = "2020.3.2"
command = f'choco install {packageName} --version {version} --yes --allowmultipleversions --ia=\'ACTIVATE_KEY="{activationKey}" REGISTER=1 AUTOUPDATE=0\''

# call the powershell/choco CLI command
commandList = shlex.split(command)
process = subprocess.Popen(commandList,stdout=subprocess.PIPE)
while True:
    output = process.stdout.readline()
    if len(output) == 0 and process.poll() is not None:
        break
    else:
        print(output.decode('utf-8'))

print(command)
print(commandList)
