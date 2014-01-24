import QtQuick 2.1

NativeText {
    property url url
    
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            Qt.openUrlExternally(url);
        }
    }
}