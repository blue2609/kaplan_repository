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

# install packages to base environment as specified by base_env.yaml
Start-Process cmd -ArgumentList @(
	"/c","powershell",
	"mamba","env","update","-f","base_env.yaml"
) -Wait

Start-Process cmd -ArgumentList @(
	"/c","powershell","./create_venvs.ps1",
	"-VenvCreationMethod",$VenvCreationMethod,
	"-RunCmdDir",$RunCmdDir
) -Wait