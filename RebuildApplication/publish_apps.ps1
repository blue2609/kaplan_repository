[CmdletBinding()]
Param(
	[parameter(Mandatory)]
	[string]$RunCmdDir
)

$publish_apps_json = Get-ChildItem "./publish_apps" | Where-Object {$_.Name -like '*.json'}
foreach ($json_file in $publish_apps_json) {
	$venv = Get-Content -Raw -Path $json_file.FullName | ConvertFrom-Json
	foreach ($app in $venv) {
		New-RDRemoteApp `
		-Collectionname "MBATS" `
		-Alias $app.alias `
		-DisplayName $app.display_name `
		-FilePath "c:\windows\system32\WindowsPowershell\v1.0\powershell.exe" `
		-RequiredCommandLine $RunCmdDir"\"$($app.display_name)".ps1" `
		-IconPath $app.icon_path `
		-ConnectionBroker kap-aws-rdsb-1.kaplan-student.edu.au
	}
}