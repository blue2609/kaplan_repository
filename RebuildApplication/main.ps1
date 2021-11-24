# Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope LocalMachine
[CmdletBinding()]
Param (
	[switch]$InstallMamba,

	[switch]$GetLatestMamba,

	[ValidateNotNullOrEmpty()]
	[string]$VenvCreationMethod = 'custom',

	[Parameter(Mandatory)]
	[string]$RunCmdDir
)

# Install mamba package manager if InstallMamba is '$true'
if ($InstallMamba) {
	if ($GetLatestmamba) {
		Start-Process cmd -ArgumentList @(
			"/c","powershell","./install_mamba.ps1","-GetLatestMamba"
		) -Wait
	} else {
		Start-Process cmd -ArgumentList @(
			"/c","powershell","./install_mamba.ps1"
		) -Wait
	}
}

Start-Process cmd -ArgumentList @(
	"/c","powershell","./create_venvs.ps1",
	"-VenvCreationMethod",$VenvCreationMethod,
	"-RunCmdDir",$RunCmdDir
) -Wait

# publish the applications
Start-Process cmd -ArgumentList @(
	"/c","powershell","./publish_apps.ps1",
	"-RunCmdDir",$RunCmdDir
) -Wait
