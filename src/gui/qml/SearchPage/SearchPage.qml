import QtQuick 2.1
import "../Widgets" as Widgets

Item {
    SearchForm {
        id: searchForm
        anchors.top: parent.top
        anchors.topMargin: 40
        anchors.horizontalCenter: parent.horizontalCenter
        z: 100
        onGrabClicked: {
            visible = false
            grabPage.visible = true
        }
        
        onQueryClicked: {
            visible = false
            resultView.visible = true
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
    
    ResultView {
        id: resultView
        visible: false
        anchors.fill: parent
        onBackClicked: {
            visible = false
            searchForm.visible = true
        }
    }
}
