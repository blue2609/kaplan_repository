# Introduction
This project aims to automate the installation of applicatoins on MBATS servers (for both prod and non-prod) 

# Program/App Structure
The goal is to have a parent program in the form of an application with user interface that can control the installation/updates/removal of MBATS applications such as Tableau, PowerBI, RStudio, R, Anaconda, etc. 

Below is the current (messy) structure of the project
```
📦AutomateAppUpdate
 ┣ 📂application
 ┃ ┣ 📂PowershellScript
 ┃ ┃ ┣ 📜getAllAppsInstalled.ps1
 ┃ ┃ ┗ 📜tableuScript.ps1
 ┃ ┣ 📜getApps.py
 ┃ ┗ 📜tableauScript.py
 ┣ 📂templates
 ┃ ┣ 📜mainPage.html
 ┃ ┗ 📜parentLayout.html
 ┣ 📜checkChocoPackage.py
 ┣ 📜flaskapp.py
 ┗ 📜readme.md
```

# Tableau Desktop Installation
For Tableau Desktop installation, the script is located under 
> application > PowershellScript > **tableuScript.ps1**

Administrator needs to pass several parameter arguments to the this powershell script such as:

- **The Tableau Desktop version** they want to install 
- The **Activation Key** to activate Tableau Desktop (assuming no other Tableau Desktop on the server had been activated) 
- The **register** number to indicate whether administrator wants to register to the Tableau Desktop installation or not:
    - Please specify `register 1` to indicate that Tableau Desktop will be reigstered during its installation 
    - Please specify `register 0` to indicate that we DON'T want Tableau Desktop to be registered during its installation 
- The **autoUpdate** number to indicate whether we want to give the ability of auto-updating Tableau Desktop (if there's any maintenance upgrade available) to server users (in this case, KBS teachers):
    - Specify `autoUpdate 1` to give Tableau Desktop the ability to automatically update itself (if there's any maintenance update) and to give users the ability to turn on/off the automatic update option in Tableau Desktop
    - Specify `autoUpdate 0` to disable Tableau Desktop automatic update. This will also disable all users ability to and to turn on/off the automatic update option in Tableau Desktop

Example of script usage:

```
.\tableuScript.ps1 -version 2021.1.2 -activationKey "xxxx-xxxx-xxxx-xxxx-xxxx" -register 1 -autoUpdate 0
```

