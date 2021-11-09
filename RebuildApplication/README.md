# Rebuilding MBATS Applications
This project contains all the PowerShell scripts to re-install data analytics applications used by KBS on a new Windows Server

`mamba_installer.exe` is included in this repository but it might not be the most up-to-date one. In order to get the latest installer, please run `mamba_download.ps1` PowerShell script to get the latest Windows mamba package manager installer from mambaforge

# Turn Off/Deactivate ZScaler
Please turn off ZScaler/deactivate it before running this script. I've tried running the script with ZScaler on my Windows Server 2022 Virtual Machine and the VM was unable connect to the internet and download the packages with ZScaler turned on. 
