#SingleInstance, force
#Persistent

Menu, Tray, Icon, keep_awake.ico
CoordMode, ToolTip, Screen
SetTimer, NoSleep, 30000
Return

NoSleep:
    DllCall( "SetThreadExecutionState", UInt,0x80000003 )
    Return

$!Esc::
    ExitApp
