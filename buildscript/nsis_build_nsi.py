nsi_script = r"""
;--------------------------------
;Include Modern UI
    ;!include "MUI2.nsh"
    !include LogicLib.nsh
;--------------------------------
;General

;--------------------------------
;Interface Settings
    !define FILES_SOURCE_PATH dist\FSETOOLS
    !define INST_LIST nsis_build_inst_list.nsh
    !define UNINST_LIST nsis_build_uninst_list.nsh
    !define APPNAME FSETOOLS
    !define COMPANYNAME OFR
    !define DESCRIPTION "Fire Safety Engineering Tools"
    ;These three must be integers
    !define VERSIONMAJOR {version_major}
    !define VERSIONMINOR {version_minor}
    !define VERSIONBUILD {version_build}
    ;These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
    ;It is possible to use "mailto:" links in here to open the email client
    !define HELPURL "https://github.com/fsepy/fsetools" ;"Support Information" link
    !define UPDATEURL "https://github.com/fsepy/fsetools" ;"Product Updates" link
    !define ABOUTURL "https://github.com/fsepy/fsetools" ;"Publisher" link
    ;Size of the program, when installed, in kb.
    !define INSTALLSIZE 137216

RequestExecutionLevel admin ;Require admin rights on NT6+ (When UAC is turned on)

InstallDir "$PROGRAMFILES\${{COMPANYNAME}}\${{APPNAME}}"

;rtf or txt file - remember if it is txt, it must be in the DOS text format (\r\n)
;LicenseData "license.rtf"
;This will be in the installer/uninstaller's title bar
Name "${{APPNAME}}"
Icon "etc\ofr_logo_1_80_80.ico"
outFile "FSETOOLS Installer.exe"

;Just three pages - license agreement, install location, and installation
;page license
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${{If}} $0 != "admin" ;Require admin rights on NT4+
        messageBox mb_iconstop "Administrator rights required!"
        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        quit
${{EndIf}}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    ;Files for the install directory - to build the installer, these should be in the same directory as the install script (this file)
    setOutPath $INSTDIR
    ;Files added here should be removed by the uninstaller (see section "uninstall")
    ;!include 'nsis_build_inst_list'
    File /r 'dist\FSETOOLS\*'
    ;Add any other files for the install directory (license files, app data, etc) here

    ;Uninstaller - See function un.onInit and section "uninstall" for configuration
    writeUninstaller "$INSTDIR\uninstall.exe"

    ;Start Menu
    createDirectory "$SMPROGRAMS\${{COMPANYNAME}}"
    createShortCut "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}.lnk" "$INSTDIR\${{APPNAME}}.exe" "" "$INSTDIR\etc\ofr_logo_1_80_80.ico"

    ;Registry information for add/remove programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayName" "${{APPNAME}}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "QuietUninstallString" "$INSTDIR\uninstall.exe /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayIcon" "$INSTDIR\etc\ofr_logo_1_80_80.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "Publisher" "${{COMPANYNAME}}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "HelpLink" "${{HELPURL}}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "URLUpdateInfo" "${{UPDATEURL}}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "URLInfoAbout" "${{ABOUTURL}}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayVersion" "${{VERSIONMAJOR}}.${{VERSIONMINOR}}.${{VERSIONBUILD}}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "VersionMajor" ${{VERSIONMAJOR}}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "VersionMinor" ${{VERSIONMINOR}}
    ;There is no option for modifying or repairing the install
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "NoRepair" 1
    ;Set the INSTALLSIZE constant (!defined at the top of this script) so Add/Remove Programs can accurately report the size
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "EstimatedSize" ${{INSTALLSIZE}}
sectionEnd

;Uninstaller

function un.onInit
    SetShellVarContext all
    
    #Verify the uninstaller - last chance to back out
    
    MessageBox MB_OKCANCEL "Permanantly remove ${{APPNAME}}?" IDOK next
        Abort
    next:
    !insertmacro VerifyUserIsAdmin
functionEnd

section "uninstall"
    ;Remove Start Menu launcher
    delete "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}.lnk"
    ;Try to remove the Start Menu folder - this will only happen if it is empty
    rmDir "$SMPROGRAMS\${{COMPANYNAME}}"
    
    ;Remove the files (using externally generated file list)
    !include ${{UNINST_LIST}}
    
    ;Always delete uninstaller as the last action
    delete $INSTDIR\uninstall.exe
    
    ;Try to remove the install directory - this will only happen if it is empty
    rmDir /r $INSTDIR
 
    ;Remove uninstaller information from the registry
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}"

sectionEnd"""

if __name__ == '__main__':
    print(nsi_script.format(version_major=1, version_minor=2, version_build=3))
