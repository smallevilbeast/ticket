import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

ButtonStyle {
    background: Rectangle {
        color: "transparent"
        implicitWidth:  backImage.width
        implicitHeight: backImage.height
        
        Image {
            id: backImage
            source: control.hovered || control.checked ? "/home/evilbeast/project/ticket/src/gui/images/common/menu_press.png" : "/home/evilbeast/project/ticket/src/gui/images/common/menu_normal.png"
            
            Column {
                anchors.centerIn: parent
                
                Image {
                    anchors.horizontalCenter: parent.horizontalCenter
                    source: "/home/evilbeast/project/ticket/src/gui/images/common/query_checked.png"
                }
                
                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "抢票"
                }
            }
        }
    }
}
