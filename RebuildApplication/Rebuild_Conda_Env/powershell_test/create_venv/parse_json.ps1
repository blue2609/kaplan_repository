
$json_path = "spyder_ide.json"
$json = Get-Content -Raw -Path $json_path | ConvertFrom-Json
ForEach ($venv in $json){
	# create and activate conda environment
	conda create --name $venv.name
	conda activate $venv.name

	ForEach ($pkg_collection in $venv.packages){
		$pkg_manager = $pkg_collection.pkg_manager
		$pkg_channel = $pkg_collection.channel

		ForEach ($pkg_name in $pkg_collection.pkg_names){
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
		# if ($pkg_channel){
		# 	$install_command = "$pkg_manager install "  + 
		# 						$($pkg_collection.pkg_names -join " ") + 
		# 						" --channel " + 
		# 						$pkg_collection.channel
		# }else{
		# 	$install_command = "$pkg_manager install "  + 
		# 						$($pkg_collection.pkg_names -join " ") 
		# }
		# Invoke-Expression $install_command
	# 	# $pkg_manager
		# $pkg_channel
		# $install_command = "$pkg_manager create --name "  + 
		# 					$venv.name + " " + 
		# 					$($pkg_collection.pkg_names -join " ") + 
		# 					" --channel " + 
		# 					$pkg_collection.channel
		# $install_command = "$pkg_manager install --name "  + 
		# 					$venv.name + " " + 
		# 					$($pkg_collection.pkg_names -join " ") + 
		# 					" --channel " + 
		# 					$pkg_collection.channel
		# $install_command
	}
}
