Set objShell = WScript.CreateObject("WScript.Shell")
 
 If(Wscript.Arguments(0)="desktop") Then
    'All users Desktop
    allUsersDesktop = objShell.SpecialFolders("AllUsersDesktop")
 
    'The current users Desktop
    usersDesktop = objShell.SpecialFolders("Desktop")
 
    'Where to create the new shorcut
    Set objShortCut = objShell.CreateShortcut(usersDesktop & "\ImaginaryInfinity Calculator.lnk")
 
    'What does the shortcut point to
    objShortCut.TargetPath = "%USERPROFILE%\ImaginaryInfinity-Calculator\launcher.bat"
 
    'Add a description
    objShortCut.Description = "ImaginaryInfinity Calculator"
    objShortCut.IconLocation = "%USERPROFILE%\ImaginaryInfinity-Calculator\iicalc.ico"
 
    'Create the shortcut
    objShortCut.Save
ElseIf (Wscript.Arguments(0)="path") Then
	Set objEnv = objShell.Environment("System")
	pathToAdd = "C:\%USERPROFILE%\.iicalc\"
	oldSystemPath = objEnv("PATH")
	newSystemPath = oldSystemPath & ";" & pathToAdd
	objEnv("PATH") = newSystemPath
Else
    path = objShell.SpecialFolders("StartMenu")
    Set link = objShell.CreateShortcut(path & "\ImaginaryInfinity Calculator.lnk")
    link.Description = "ImaginaryInfinity Calculator"
    link.TargetPath = "%USERPROFILE%\ImaginaryInfinity-Calculator\launcher.bat"
    link.IconLocation = "%USERPROFILE%\ImaginaryInfinity-Calculator\iicalc.ico"
    'link.WorkingDirectory = "dir"
    link.Save
End If
