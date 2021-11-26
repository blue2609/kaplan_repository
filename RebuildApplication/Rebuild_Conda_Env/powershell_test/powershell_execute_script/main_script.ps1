# Invoke-Command { & "powershell" ./child_script.ps1 `
# 				   				-firstWord 'stanley' `
# 								-secondWord 'setiawan'}

$firstWord = 'stanley'
$secondWord = 'setiawan'
invoke-expression "cmd /c start powershell -NoExit -Command {                           `
    ./child_script.ps1 -firstWord $firstWord -secondWord $secondWord;                  `
}";                                                      
