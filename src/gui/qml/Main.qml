import QtQuick 2.1
import "Common" as Common
import "LoginPage" as LoginPage
import "SearchPage" as SearchPage
import "Widgets" as Widgets

Common.DWindow {
    width: 500; height: 500
    signal showErrorInfo(string info)
    Component.onCompleted: {
        Poster.errorExcepted.connect(showErrorInfo)
    }
    onShowErrorInfo: errorTooltip.show(info)
    
    
    Item {
        anchors.fill: parent
        
        Connections {
            target: Poster
            onLoginSuccessed: {
                loginPage.visible = false
                searchPage.visible = true
            }
        }

        Widgets.Tooltip {
            id: errorTooltip
            anchors.top: parent.top
            anchors.topMargin: -1
            anchors.horizontalCenter: parent.horizontalCenter
            z: 1000
        }
        LoginPage.LoginPage {id: loginPage;  anchors.fill: parent }
        SearchPage.SearchPage { id: searchPage; anchors.fill: parent; visible: false }
    }
    
}