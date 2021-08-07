There are 3 Powershell scripts in this project:

- `checkExploratoryProcess.ps1` is the script which should be used as target for remoteapp with RDS. This script will open up Exploratory Desktop application IF no other user is using Exploratory Desktop on the server. Otherwise, this script will launch a window that says "**Exploratory is being used by another user on the server**"
- `powerShellGUI.ps1` is used to test the GUI design for this script
- `stopExploratoryProcess.ps1` is the script which will be used to kill the **exploratory.exe** in between classes/regular maintenance hours. This script must be executed by the server administrator, it requires admin level of permission