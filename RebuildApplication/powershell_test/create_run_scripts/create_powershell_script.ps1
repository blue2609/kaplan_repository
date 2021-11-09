$json_path = "conda_venv.json"
$json = Get-Content -Raw -Path $json_path | ConvertFrom-Json

ForEach($venv in $json){
	# create a powershell script to open application in 
	# each corresponding virtual environment created

	$venv_startdir = $venv.start_dir
	$venv_name = $venv.name
	$app_run_command = $venv.run_command
	$run_application = 
@"
Set-Location $venv_startdir
mamba run --name $venv_name $app_run_command
"@

    $run_application | Out-File -FilePath $venv_name".ps1"
}