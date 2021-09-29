New-RDRemoteApp -Collectionname "MBATS" `
-Alias "Orange" `
-DisplayName "Orange" `
-filePath "C:\Program Files\Orange\pythonw.exe" `
-CommandLineSetting Require `
-IconPath "C:\Program Files\Orange\share\orange3\icons\Orange.ico" `
-RequiredCommandLine "-m Orange.canvas" `
-ConnectionBroker kap-aws-rdsb-1n.non-prod.kaplan-student.edu.au