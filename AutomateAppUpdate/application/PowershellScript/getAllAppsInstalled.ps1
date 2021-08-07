# get path to the csv File
param($csvFilePath)

# query the list of apps with Get-WmiObject 
Get-WmiObject -Class Win32_Product | Select-Object -Property Name,Version,InstallLocation,InstallDate | Export-Csv -Path $csvFilePath -NoTypeInformation

# query the list of apps from registry
$registryPath = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
$registryParameter = @{
    Property =  @{Name="Name";Expression={$_.DisplayName}},
                @{Name="Version";Expression={$_.DisplayVersion}},
                'InstallLocation',
                'InstallDate'
}

Get-ItemProperty $registryPath | Select-Object @registryParameter | Export-Csv -Append -Path $csvFilePath