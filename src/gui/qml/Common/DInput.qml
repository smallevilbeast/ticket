import QtQuick 2.1

ShadowPanel {
	width: 260; height: 42
	property alias echoMode: input.echoMode
    property alias text: input.text
    property alias font: input.font
    property var textInput: input
    signal returnPressed
    
	TextInputShadow {
		id: input
		width: parent.width - 20
        /* height: parent.height - 8 */
		anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
		verticalAlignment: Qt.AlignCenter
		clip: true
        focus: true
        Keys.onReturnPressed: returnPressed()
        font.pixelSize: 16
	}
    
	
}
