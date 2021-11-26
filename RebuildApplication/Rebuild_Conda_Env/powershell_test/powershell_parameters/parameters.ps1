function Test-MrParameter {
	param (
		$ComputerName
	)

	Write-Output $ComputerName
}

function Get-MrParameterCount {
	param (
		[string[]]$ParameterName
	)

	foreach ($Parameter in $ParameterName) {
		$Results = Get-Command `
				   -ParameterName $Parameter `
				   -ErrorAction	SilentlyContinue
		
		[pscustomobject]@{
			ParameterName = $Parameter
			NumberOfCmdlets = $Results.Count
		}
	}
}

function Test-MrCmdletBinding {
	[CmdletBinding()] #<<-- This turns a regular function into an advanced function
	param (
		$ComputerName
	)

	Write-Output $ComputerName
}

function Test-MrParameterValidation {
	<#
	.SYNOPSIS
		Returns a list of services that are set to start automatically, are not
		currently running, excluding the services that are set to delayed start.

	.DESCRIPTION
		Get-MrAutoStoppedService is a function that returns a list of services from
		the specified remote computer(s) that are set to start automatically, are not
		currently running, and it excludes the services that are set to start automatically
		with a delayed startup.

	.PARAMETER ComputerName
		The remote computer(s) to check the status of the services on.

	.PARAMETER Credential
		Specifies a user account that has permission to perform this action. The default
		is the current user.

	.EXAMPLE
		Get-MrAutoStoppedService -ComputerName 'Server1', 'Server2'

	.EXAMPLE
		'Server1', 'Server2' | Get-MrAutoStoppedService

	.EXAMPLE
		Get-MrAutoStoppedService -ComputerName 'Server1' -Credential (Get-Credential)

	.INPUTS
		String

	.OUTPUTS
		PSCustomObject

	.NOTES
		Author:  Mike F Robbins
		Website: http://mikefrobbins.com
		Twitter: @mikefrobbins
	#>
	[CmdLetBinding()]
	param (
		# [Parameter(Mandatory)]
		[ValidateNotNullOrEmpty()]
		[string[]]$ComputerName = $env:COMPUTERNAME
	)

	Write-Output $ComputerName
}

function Test-MrVerboseOutput {
	[CmdLetBinding()]
	param (
		[ValidateNotNullOrEmpty()]
		[string[]]$ComputerName = $env:COMPUTERNAME
	)
	foreach ($Computer in $ComputerName) {
		Write-Verbose -Message "Attempting to perform some action on $Computer"
		Write-Output $Computer
	}
}