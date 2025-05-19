
set clsid=%1

reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\%clsid% /f
reg delete HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\%clsid% /f
reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\%clsid% /f
reg delete HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\%clsid% /f
reg delete HKCU\Software\Classes\CLSID\%clsid% /f
reg delete HKCR\CLSID\%clsid% /f
reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\%clsid% /f
reg delete HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\%clsid% /f