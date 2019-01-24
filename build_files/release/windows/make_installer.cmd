ECHO Make OCVL installer


SET NSIS_COMMAND="C:\Program Files (x86)\NSIS\makensis"
SET NSIS_SCIRPT_PATH="C:\Users\Dom\build_blender\blender\release\windows\installer\00.sconsblender.nsi"


SET RELDIR="C:\Users\Dom\build_blender\blender\release\windows\installer"
SET DISTDIR="C:\Users\Dom\build_blender\build_windows_Lite_x64_vc15_Release\bin\Release"
SET VERSION="1.2.0.1"
SET ROOTDIRCONTS="C:\Users\Dom\build_blender\build_windows_Lite_x64_vc15_Release\bin\Release"

ECHO %NSIS_EXE_PATH%
CALL %NSIS_COMMAND% ^
    /DDISTDIR="%DISTDIR%" ^
    /DRELDIR="%RELDIR%" ^
    /DVERSION="%VERSION%" ^
    /DROOTDIRCONTS="%ROOTDIRCONTS%" ^
    %NSIS_SCIRPT_PATH%