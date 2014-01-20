import QtQuick 2.1
import "../Widgets" as Widgets

Item {
    SearchForm {
        id: searchForm
        anchors.top: parent.top
        anchors.topMargin: 40
        
        anchors.horizontalCenter: parent.horizontalCenter
        z: 100
        onClicked: {
            visible = false
            grabPage.visible = true
        }
        
    }
    
    GrabPage {
        anchors.fill: parent
        id: grabPage
        visible: false
        onClicked: {
            visible = false
            searchForm.visible = true
        }
    }
    
}
