import QtQuick 2.1
import "../Common" as Common

Rectangle {
    id: container
    width: row.width + 16; height: row.height + 16
    property alias text: message.text
    property alias font: message.font
    property alias textColor: message.color
    color: "#ffffe5"
    visible: false
    border { width: 1; color: "#c6c600" }
    
    function show(text) {
        message.text = text
        container.visible = true
        timer.restart()
    }
    
    function hide() {
        timer.stop()
        container.visible = false
    }
    
    Row {
        id: row
        anchors.centerIn: parent
        spacing: 20
        
        Text {
            id: message
            color: "#ef3f22"
            anchors.verticalCenter: parent.verticalCenter
        }

        Common.ImageButton {
            normalImage: "qrc:/images/common/small_close_normal.png"
            hoverImage: "qrc:/images/common/small_close_press.png"
            pressImage: "qrc:/images/common/small_close_press.png"
            anchors.verticalCenter: parent.verticalCenter
            onClicked: hide()
        }
    }
    
    Timer {
        id: timer
        interval: 5000
        onTriggered: {
            container.visible = false
        }
    }
}