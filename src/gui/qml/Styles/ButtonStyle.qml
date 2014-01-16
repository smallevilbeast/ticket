import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

ButtonStyle {
    background: Rectangle {
        implicitWidth:  control.width
        implicitHeight: control.height
        /* color: control.pressed ?  "#106892" : "#1790c9" */
        color: control.pressed ?  "#669900" : "#87ca00"
        radius: 3
    }
    
    label: Text {
        text: control.text
        color: "#fff"
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: 14
    }
}
