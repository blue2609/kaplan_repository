[CmdletBinding()]
param (
	[switch]$GetLatestMamba
)

if ($GetLatestMamba) {
	Invoke-WebRequest `
	-Uri "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Windows-x86_64.exe" `
	-OutFile "mamba_installer.exe"
}

Start-Process `
-FilePath "./mamba_installer.exe" `
-ArgumentList "/S" `
-Wait

# Add relevant mamba and conda paths to $env:Path environment variable to make
# conda and mamba accessible from PowerShell and Command Prompt
$mamba_root_dir = "C:\ProgramData\mambaforge"
$mamba_paths = @(
	($mamba_root_dir),
	($mamba_root_dir + "\condabin"),
	($mamba_root_dir + "\Library\bin"),
	($mamba_root_dir + "\Library\usr\bin"),
	($mamba_root_dir + "\Library\mingw-w64\bin"),
	($mamba_root_dir + "\Scripts")
)
$env:Path += $mamba_paths -join ";"
[System.Environment]::SetEnvironmentVariable('Path',$env:Path,'Machine')

# change conda config so virtual env can work together better with pip 
conda config --set pip_interop_enabled True

# initialise conda
conda init