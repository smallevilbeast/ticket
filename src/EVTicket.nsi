# EVTicket NSIS installer script.

# contants
!define EVTICKET_VERSION       "0.9"
!define EVTICKET_NAME          "EVTicket"
!define EVTICKET_HK_ROOT       "Software\EVTicket"
!define EVTICKET_HK            "${EVTICKET_HK_ROOT}\InstallPath"
!define EVTICKET_CN_NAME       "EV抢票助手"

# Include the tools we use.
!include MUI2.nsh
!include LogicLib.nsh

# Tweak some of the standard pages.
!define MUI_WELCOMEPAGE_TEXT \
"This wizard will guide you through the installation of ${EVTICKET_NAME}.$\r$\n $\r$\n Click Next to continue."

!define MUI_FINISHPAGE_LINK "访问作者博客"
!define MUI_FINISHPAGE_LINK_LOCATION "http://smallbeast.duapp.com"

# Define the product name and installer executable.
Name "${EVTICKET_NAME}"
Caption "${EVTICKET_NAME} Setup"
OutFile "${EVTICKET_NAME}-${EVTICKET_VERSION}.exe"
installDir "$PROGRAMFILES\${EVTICKET_NAME}"
InstallDirRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${EVTICKET_NAME}" "UninstallString"

# This is done (along with the use of SetShellVarContext) so that we can remove
# the shortcuts when uninstalling under Vista and Windows 7.  Note that we
# don't actually check if it is successful.
RequestExecutionLevel admin

# Maximum compression.
SetCompressor /SOLID lzma

# We want the user to confirm they want to cancel.
!define MUI_ABORTWARNING
!define MUI_ICON "gui\images\common\logo.ico" 

# Define the different pages.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_COMPONENTS

!define MUI_DIRECTORYPAGE_TEXT_DESTINATION "EVTicket installation folder"
!define MUI_DIRECTORYPAGE_TEXT_TOP \
"EVTicket will be installed in the $INSTDIR folder"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES


# Other settings.
!insertmacro MUI_LANGUAGE "English"


Section "主程序" SecModules
    SectionIn 1 2 RO

    SetOverwrite on

    SetOutPath $INSTDIR
    File /r .\dist\*
SectionEnd


Section "Start Menu shortcuts" SecShortcuts
    SectionIn 1

    SetShellVarContext all

    # Make sure this is clean and tidy.
    RMDir /r "$SMPROGRAMS\${EVTICKET_CN_NAME}"
    CreateDirectory "$SMPROGRAMS\${EVTICKET_CN_NAME}"

    IfFileExists "$INSTDIR\${EVTICKET_NAME}.exe" 0 +4
        CreateShortCut "$SMPROGRAMS\${EVTICKET_CN_NAME}\${EVTICKET_NAME}.lnk" "$INSTDIR\${EVTICKET_NAME}.exe"
        CreateShortCut "$SMPROGRAMS\${EVTICKET_CN_NAME}\作者博客.lnk" "http://smallbeast.duapp.com/"
        CreateShortCut "$SMPROGRAMS\${EVTICKET_CN_NAME}\Uninstall ${EVTICKET_NAME}.lnk" "$INSTDIR\Uninstall.exe"
        CreateShortcut "$DESKTOP\${EVTICKET_CN_NAME}.lnk" "$INSTDIR\${EVTICKET_NAME}.exe"
SectionEnd


Section "Uninstall"
    SetShellVarContext all

    # The modules section.
    RMDir /r $INSTDIR

    # The shortcuts section.
    RMDir /r $SMPROGRAMS\${EVTICKET_CN_NAME}

    # The desktop link file.
    Delete $DESKTOP\${EVTICKET_CN_NAME}.lnk

    # Clean the registry.
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${EVTICKET_NAME}"
    DeleteRegKey HKLM "${EVTICKET_HK_ROOT}"
    DeleteRegKey HKCU "${EVTICKET_HK_ROOT}"
SectionEnd


Section -Post
    # Add the bin directory to PATH.
    # Push $INSTDIR
    # Call AddToPath

    # Tell Windows about the package.
    # WriteRegExpandStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${EVTICKET_NAME}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${EVTICKET_NAME}" "DisplayName" "${EVTICKET_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${EVTICKET_NAME}" "DisplayVersion" "${EVTICKET_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${EVTICKET_NAME}" "NoModify" "1"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${EVTICKET_NAME}" "NoRepair" "1"

    # Save the installation directories for the uninstaller.
    # ClearErrors
    WriteRegStr HKLM "${EVTICKET_HK}" "" "$INSTDIR"
    
    # IfErrors 0 +2
    WriteRegStr HKCU "${EVTICKET_HK}" "" "$INSTDIR"

    # Create the uninstaller.
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd


# Section description text.
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecModules} \
"The EVTicket main modules."
!insertmacro MUI_DESCRIPTION_TEXT ${SecShortcuts} \
"This adds shortcuts to your Start Menu."
!insertmacro MUI_FUNCTION_DESCRIPTION_END



Function .onInit
    # Check if there is already a version of EVTicket installed for this version
    # of Python.
    ReadRegStr $0 HKCU "${EVTICKET_HK}" ""

    ${If} $0 == ""
        ReadRegStr $0 HKLM "${EVTICKET_HK}" ""
    ${Endif}

    ${If} $0 != ""
        MessageBox MB_YESNO|MB_DEFBUTTON2|MB_ICONQUESTION \
"A copy of ${EVTICKET_NAME} is already installed in $0 \
and should be uninstalled first.$\r$\n $\r$\n\ Do you wish to uninstall it?" IDYES Uninstall
            Abort
Uninstall:
        ExecWait '"$0\Uninstall.exe" /S'
    ${Endif}
FunctionEnd
