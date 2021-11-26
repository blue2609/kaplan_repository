param (
	[switch]$SomeParameter
)

function SomeFunction {
	param (
		[switch]$SomeParameter
	)

	if ($SomeParameter) { 
		Write-Output "Parameter is passed to the function"
	}
}

SomeFunction