#Persistent
Gui, Add, Text, x20 y20 w300 h30, Personalization
Gui, Add, Button, x20 y60 w100 h30 gSelectBackground, Background
Gui, Add, Button, x150 y60 w100 h30 gDefaults, Defaults
Gui, Show, w300 h120, Settings Menu

Return

SelectBackground:
; Allow selecting PNG, JPEG, and BMP files
FileSelectFile, SelectedFile, 3, , Select a Background, Images (*.png;*.jpeg;*.jpg;*.bmp)
If (SelectedFile != "")
{
    ; Copy the selected file to the BGU path (without changing its extension)
    NewFilePath := "C:\TAOS\RESOURCES\BGU"  ; Save as the original file name without changing extension
    FileCopy, %SelectedFile%, %NewFilePath%, 1
    MsgBox, File copied to %NewFilePath%
}
Else
{
    MsgBox, No file selected.
}
Return

Defaults:
; Define any default actions you want here
MsgBox, Default settings are applied.
Return

GuiClose:
ExitApp
