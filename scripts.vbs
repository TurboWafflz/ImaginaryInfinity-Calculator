Set objShell = WScript.CreateObject("WScript.Shell")
 If(Wscript.Arguments(0)="desktop") Then
    'All users Desktop
    allUsersDesktop = objShell.SpecialFolders("AllUsersDesktop")

    'The current users Desktop
    usersDesktop = objShell.SpecialFolders("Desktop")

    'Where to create the new shorcut
    Set objShortCut = objShell.CreateShortcut(usersDesktop & "\ImaginaryInfinity Calculator.lnk")

    'What does the shortcut point to
    objShortCut.TargetPath = "C:\Program Files (x86)\iicalc\launcher.bat"

    'Add a description
    objShortCut.Description = "ImaginaryInfinity Calculator"
    objShortCut.IconLocation = "C:\Program Files (x86\iicalc\iicalc.ico"

    'Create the shortcut
    objShortCut.Save
ElseIf (Wscript.Arguments(0)="path") Then
	Set objEnv = objShell.Environment("System")
	pathToAdd = "C:\Program Files (x86)\iicalc\"
	oldSystemPath = objEnv("PATH")
	newSystemPath = oldSystemPath & ";" & pathToAdd
	objEnv("PATH") = newSystemPath
ElseIf (Wscript.Arguments(0)="startmenu") Then
    path = objShell.SpecialFolders("StartMenu")
    Set link = objShell.CreateShortcut(path & "\ImaginaryInfinity Calculator.lnk")
    link.Description = "ImaginaryInfinity Calculator"
    link.TargetPath = "C:\Program Files (x86)\iicalc\launcher.bat"
    link.IconLocation = "C:\Program Files (x86)\iicalc\iicalc.ico"
    'link.WorkingDirectory = "dir"
    link.Save
ElseIf (Wscript.Arguments(0)="uninstall") Then
    usersDesktop = objShell.SpecialFolders("Desktop")
		startmenu = objShell.SpecialFolders("StartMenu")
		Set fs = CreateObject("Scripting.Filesystemobject")
		If (fs.FileExists(usersDesktop & "\ImaginaryInfinity Calculator.lnk")) Then
				fs.DeleteFile( usersDesktop & "\ImaginaryInfinity Calculator.lnk" )
		End If
		If (fs.FileExists(startmenu & "\ImaginaryInfinity Calculator.lnk")) Then
				fs.DeleteFile( startmenu & "\ImaginaryInfinity Calculator.lnk" )
		End If

End If
