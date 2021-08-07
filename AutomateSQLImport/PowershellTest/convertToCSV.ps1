param ($excelFileName,$sheetName,$saveLocation=$pwd)

$sheetName
Function ExcelToCsv($excelFileName){
    # Try to convert this one to csv file
    $Excel = New-Object -ComObject Excel.Application
    # $excelDir= ""

    # $excelFile = $excelDir + $excelFileName + ".xlsx"
    # $wb = $Excel.Workbooks.Open($excelFile)
    $wb = $Excel.Workbooks.Open("$pwd\$excelFileName" + ".xlsx")
    # $noExcelWorksheets = $wb.Worksheets.Count

    Write-Host("The name of the file is [$excelFileName]")
    Write-host("The number of worksheets in the excel file is $($wb.Worksheets.Count)")

    foreach($ws in $wb.Worksheets){
        $worksheet_name = $ws.Name
        $ws.SaveAs("$saveLocation\$excelFileName\$worksheet_name" + ".csv",6)
    }
    $Excel.Quit()
}

# Write-Host("The Excel File name is [$excelFilename]")
ExcelToCsv($excelFileName)
