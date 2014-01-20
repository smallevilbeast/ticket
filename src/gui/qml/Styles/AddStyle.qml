import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

ButtonStyle {
    background: Rectangle {
        implicitWidth:  image.width
        implicitHeight: image.height
        color: "transparent"
        border { width: 1; color: control.enabled ? control.hovered ? "#0B76BA" : "#3BA2E3" : "#BABABA"}
        Image {
            id: image
            width: 18; height: 18
            source: control.enabled ? control.hovered ? "qrc:/images/common/icon_add_hover.png" : "qrc:/images/common/icon_add_normal.png" : "qrc:/images/common/icon_add_disable.png"
        }
    }
}
