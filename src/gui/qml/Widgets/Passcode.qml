import QtQuick 2.1
import "../Common" as Common

Rectangle {
    id: root
    color: Qt.rgba(0.3, 0.3, 0.3, 0.8)
    property string module
    property bool checkEnabled: true
    property alias codeFocus: passcode.focus
    property alias text: passcode.text
    signal closeClicked
    signal returnPressed
    signal passcodeSuccessed
    signal passcodeUpdated
    signal passcodeNewed(string module, string url)
    signal passcodeChecked(string module)
    
    Component.onCompleted: {
        Poster.passcodeNewed.connect(passcodeNewed)
        Poster.passcodeChecked.connect(passcodeChecked)
    }
        
    onPasscodeNewed: {
        if (module == root.module) {
            passcodeImage.source = url
            passcodeUpdated()
        }
    }
    
    onPasscodeChecked: {
        if (module == root.module) {
            passcodeSuccessed()
        }
    }
    
    Rectangle {
        width: 250; height: 110
        anchors.centerIn: parent
        color: "#fff"
        border { width: 1; color: "#0094dc" }
            
        Common.ImageButton {
            normalImage: "qrc:/images/common/small_close_normal.png"
            hoverImage: "qrc:/images/common/small_close_press.png"
            pressImage: "qrc:/images/common/small_close_press.png"
            anchors.right: passcodeColumn.right
            anchors.top: passcodeColumn.top
            onClicked: {
                closeClicked()
            }
        }
             
        Column {
            id: passcodeColumn
            anchors.centerIn: parent
            spacing: 10
                
            Text {
                text: "因12306屏蔽工具, 您需要手动输入"
                color: "#39a954"
            }
                
            Row {
                spacing: 5
                TextField {
                    id: passcode
                    width: 100
                    height: 30
                    anchors.verticalCenter: parent.verticalCenter
                    onLengthChanged: {
                        if (!checkEnabled) {
                            return
                        }
                        if (length == 4) {
                            Poster.checkPasscode(passcode.text, module)
                        }
                    }
                    Keys.onReturnPressed: {
                        root.returnPressed()
                    }
                }
            
                Image {
                    id: passcodeImage
                    /* source: Poster.passcodeUrl */
                    anchors.verticalCenter: parent.verticalCenter
                    height: passcode.height - 2
                    onSourceChanged: passcode.text = ""
                    
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            Poster.newPasscode(module)
                        }
                        cursorShape: Qt.PointingHandCursor
                    }
                }
            }
                
            Text {
                text: "12306的cookie有效期很短, Fuck 12306!!!"
                color: "#f08400"
            }
        }
    }
}
