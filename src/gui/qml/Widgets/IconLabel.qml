import QtQuick 2.1

Rectangle {
    property alias source: icon.source
    color: "#23a7e5"
    
    Image {
        id: icon
        anchors.centerIn: parent
    }
}
