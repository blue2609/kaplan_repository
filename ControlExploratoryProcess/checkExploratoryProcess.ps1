# Initialise Powershell GUI
Add-Type -AssemblyName System.Windows.Forms 

# Create a new form
$formObject = New-Object system.Windows.Forms.Form
$formObject.ClientSize = '500,300'
$formObject.text = 'Exploratory Desktop Error'
$formObject.BackColor = '#ffffff'

# Check if Exploratory Desktop is running
$exploratoryProcess = Get-Process -Name 'Exploratory' -ErrorAction SilentlyContinue

if($exploratoryProcess){
#get user
get-content -Tail 1 C:\Users\Public\Documents\exp.txt > C:\Users\Public\Documents\exp2.txt 
$user= Get-Content C:\Users\Public\Documents\exp2.txt | 
   %{ $_.Split(" ",[StringSplitOptions]"RemoveEmptyEntries")[0] }

	$message = 'Exploratory is being used by '

	# Create form description 
	$description = New-Object system.Windows.Forms.Label
	$description.text = "$message $user"
	$description.AutoSize = $true
	$description.Font = 'Microsoft Sans Serif, 13'
	$description.location = New-Object System.Drawing.Point(50,50)

	$formObject.controls.AddRange(@($description))

	$result = $formObject.ShowDialog()
} else {
	Start-Process 'C:\Program Files\Exploratory\Exploratory.exe'
	Write-Output "$env:username" | Out-file C:\Users\Public\Documents\exp.txt

}