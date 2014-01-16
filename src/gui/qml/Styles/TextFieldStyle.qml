import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0


TextFieldStyle {
    background: Rectangle {
        implicitWidth:  control.width
        implicitHeight: control.height
        color: "transparent"
        antialiasing: true
        border.color: control.pressed ? "gray" : control.activeFocus ? "#23a7e5" : "#aaaaaa"
        radius: control.radius
        
        Rectangle {
            anchors.fill: parent
            anchors.margins: 1
            color: "transparent"
            antialiasing: true
            visible: !control.pressed
            border.color: "#aaffffff"
            radius: control.radius
        }
    }
}