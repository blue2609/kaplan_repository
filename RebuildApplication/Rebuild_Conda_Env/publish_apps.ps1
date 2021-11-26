[CmdletBinding()]
Param(
	[parameter(Mandatory)]
	[string]$RunCmdDir
)

$publish_app_config = Get-Content -Raw -Path ./publish_apps_config.json | ConvertFrom-Json
$CollectionName = $publish_app_config.CollectionName
$ConnectionBroker = $publish_app_config.ConnectionBroker

$publish_apps_json = Get-ChildItem "./publish_apps" | Where-Object {$_.Name -like '*.json'}
foreach ($json_file in $publish_apps_json) {
	$venv = Get-Content -Raw -Path $json_file.FullName | ConvertFrom-Json
	foreach ($app in $venv) {
		$full_icon_path = (Join-Path $PWD $app.icon_path) | Resolve-Path
		New-RDRemoteApp `
		-Collectionname $CollectionName `
		-Alias $app.alias `
		-DisplayName $app.display_name `
		-FilePath "c:\windows\system32\WindowsPowershell\v1.0\powershell.exe" `
		-CommandLineSetting Require `
		-RequiredCommandLine $RunCmdDir"\"$($app.display_name)".ps1" `
		-IconPath $full_icon_path `
		-ConnectionBroker $ConnectionBroker
	}
}
