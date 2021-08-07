# $exploratoryProcess = Get-Process -Name 'Exploratory' -IncludeUserName | Sort-Object -Property 'UserName' 
# $exploratoryProcess = Get-Process -Name 'Exploratory' -IncludeUserName | Group-Object -Property 'UserName' | Measure-Object
$exploratoryProcess = Get-Process -Name 'Exploratory' -IncludeUserName | Group-Object -Property 'UserName' 
$exploratoryUserCount = $exploratoryProcess | Measure-Object -Line | Select-Object -ExpandProperty 'Lines'
# $exploratoryUserCount = $exploratoryProcess.Count
$exploratoryUserName = $exploratoryProcess.Name

Write-Output("There are [$exploratoryUserCount] users using Exploratory on the server")
Write-Output("===============================================================")

foreach($username in $exploratoryUserName){
    # $cleanUserName = $username | Select-String -Pattern "(?<=\\).*"
    # Write-Output("$username is using Exploratory")
    $cleanUserName = $username.Split("\")[1]
    Write-Output("[$cleanUserName]")
}


# $measureObject = $exploratoryProcess.Name | Measure-Object
# $measureObject
# $exploratoryProcess | Get-Member | Sort-Object -Property 'Name'
# if($exploratoryProcess){
#     $exploratoryProcess.UserName | Group-Object
# }