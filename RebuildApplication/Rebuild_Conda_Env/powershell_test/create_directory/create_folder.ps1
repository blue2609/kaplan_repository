param (
	[Parameter(Mandatory)]
	[string]$DirPath
)
if (!(Test-Path -path $DirPath)) {
	Write-Output("There is no directory at path $DirPath")
	New-Item -ItemType Directory -Path $DirPath
} else {
	Write-Output("$DirPath exists")
}