# Write-Host "Welcome to string to date conversion example"
# $string = '11/11/2019'
# Write-Host "The variable type now is" $string.GetType()
# $string=[Datetime]::ParseExact($string,'MM/dd/yyyy',$null)
# Write-Host "After conversion the type is" $string.GetType() " and the value is" $string

# Get-ChildItem | Format-Table -Property @{n='customColumn';e={$_.LastWriteTime.GetType()}}

# Write-Host "Date in long date format" -ForegroundColor DarkYellow
# Get-Date -Format D
# Write-Host "long date short time" -ForegroundColor DarkYellow
# Get-Date -Format f
# Write-Host "long date long time" -ForegroundColor DarkYellow
# Get-Date -Format F
# Write-Host "Date in general date time short format" -ForegroundColor DarkYellow
# Get-Date -Format g
# Write-Host "Date in general date time long format" -ForegroundColor DarkYellow
# Get-Date -Format G
# Write-Host "month day format" -ForegroundColor DarkYellow
# Get-Date -Format m
# Write-Host "Date in year format" -ForegroundColor DarkYellow
# Get-Date -Format y

# Write-Host "String to Date conversion examples"
# Write-Host "example of yymmddhhmm format"
# [System.DateTime]::ParseExact('1605221412','yyMMddHHmm',$null)
# Write-Host "Global time example"
# [System.DateTime]::ParseExact('1805221412','yyMMddHHmm',[System.Globalization.DateTimeFormatInfo]::CurrentInfo)
# Get-ChildItem | Select-Object -Property Name,LastWriteTime | Export-Csv -path 'C:\Users\stanley.setiawan\Documents' 