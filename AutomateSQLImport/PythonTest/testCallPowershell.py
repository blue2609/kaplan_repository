import subprocess 

process = subprocess.Popen(['Powershell','convertToCSV.ps1','-excelFileName','Financial_data.xlsx'],stdout=subprocess.PIPE)
output = process.communicate()[0]
print(output)


