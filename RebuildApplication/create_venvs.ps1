Param (
	[ValidateNotNullOrEmpty()]
	[string]$VenvCreationMethod = 'custom',
	[Parameter(Mandatory)]
	[string]$RunCmdDir
)

function Add-VenvFromJson {
	$venvs_json = Get-ChildItem "./virtual_envs/json"
	foreach ($json_file in $venvs_json) {
		$venv = Get-Content -Raw -Path $json_file.FullName | ConvertFrom-Json

		# create and activate conda environment
		conda create --name $venv.name --yes
		conda activate $venv.name

		foreach ($pkg_collection in $venv.packages){
			$pkg_manager = $pkg_collection.pkg_manager
			$pkg_channel = $pkg_collection.channel

			foreach ($pkg_name in $pkg_collection.pkg_names){
				if ($pkg_channel){
					$install_command = "$pkg_manager install "  + 
										$pkg_name + 
										" --channel " + 
										$pkg_collection.channel +
										" --yes"
				}else{
					$install_command = "$pkg_manager install "  + 
										$pkg_name
				}
				Invoke-Expression $install_command
			}
		}
	}
}

function Add-VenvFromYaml {
	$venvs_yaml = Get-ChildItem "./virtual_envs/yaml" 
	foreach($yaml_file in $venvs_yaml){
		$yaml_path = "./virtual_envs/$($yaml_file.Name)"
		mamba env create -f $yaml_path
	}
}

function Add-Venv {
	[CmdletBinding()]
	param (
		[Parameter(Mandatory)]
		[string]$VenvCreationMethod 
	)
	if ($VenvCreationMethod -eq 'custom'){
		Add-VenvFromJson
	}elseif ($method -eq 'default') {
		Add-VenvFromYaml
	}
}

function Add-AppRunScripts {
	[CmdletBinding()]
	param (
		[Parameter(Mandatory)]
		[string]$RunCmdDir
	)

	$venvs_json = Get-ChildItem "./virtual_envs/json"

	# create $RunCmdDir if the directory does not exist
	if (!(Test-Path -Path $RunCmdDir)) {
		New-item -ItemType Directory -Path $RunCmdDir
	}

	foreach ($json_file in $venvs_json) {
		$venv = Get-Content -Raw -Path $json_file.FullName | ConvertFrom-Json
		$run_application = 
@"
Set-Location $($venv.start_dir)
mamba run --name $($venv.name) $($venv.run_command)
"@
		$run_application | Out-File -FilePath $RunCmdDir"\"$($venv.name)".ps1" -Force
	}
}

# Create Data Analytics Virtual Envs
Add-Venv -VenvCreationMethod $VenvCreationMethod

Add-AppRunScripts -RunCmdDir $RunCmdDir