import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import "../Widgets" as Widgets
import "../Styles" as Styles
import "../Common" as Common

Item {
    property int columnHeight: 36    
    property int columnWidth: 250
    property bool codeVisible: false
    
    /* CloseButton { */
    /*     anchors.top: parent.top */
    /*     anchors.right: parent.right */
    /*     anchors.rightMargin: 1 */
    /*     visible: !codeVisible */
    /* } */
    
    function checkLogin() {
        loginButton.text = "正在努力登录中..."        
        Poster.checkLogin(username.text, passwd.text)
    }
    
    function enableLogin() {
        loginButton.text = "登录"
    }
    
    Component.onCompleted: {
        var userObj = Poster.userHistoryModel().getLastUser()
        if (userObj != undefined) {
            username.text = userObj.username
            passwd.text = userObj.password
            /* checkLogin() */
        }
    }
    
    Connections {
        target: Poster
        onPasscodeNewed: {
            codeVisible = true
            passcode.focus = true
        }
        onPasscodeChecked: {
            codeVisible = false
            Poster.login(passcode.text)
        }
    }
    
    ColumnLayout {
        id: loginLayout
        anchors.centerIn: parent
        spacing: 10
        visible: !codeVisible
                
        Row {
            spacing: -2
            Widgets.IconLabel {
                source: "qrc:/images/common/person.png"
                width: columnHeight; height: columnHeight
                radius: 3
                z: 2
            }
            
            Widgets.TextField {
                id: username
                width: columnWidth - columnHeight; height: columnHeight
                focus: true
            }
            
        }
        
        Row {
            spacing: -2
            Widgets.IconLabel {
                source: "qrc:/images/common/passwd.png"
                width: columnHeight; height: columnHeight
                radius: 3
                z: 2
            }
            
            Widgets.TextField {
                id: passwd
                width: username.width; height: columnHeight
                echoMode: TextInput.Password 
                Keys.onReturnPressed:  checkLogin()
            }
            
        }
        
        
        Row {
            spacing: 80
            
            CheckBox {
                text: "下次自动登录"
                anchors.verticalCenter: parent.verticalCenter
                checked: true
            }
            
            Widgets.LinkButton {
                text: "还没有帐号"
                color: "#0094dc"
                anchors.verticalCenter: parent.verticalCenter
            }

        }
        
        Widgets.Button {
            id: loginButton
            width: columnWidth; height: columnHeight
            text: "登录"
            onClicked: checkLogin()
        }
        
    }
    
    
    Rectangle {
        id: passcodeMask
        anchors.fill: parent
        color: Qt.rgba(0.3, 0.3, 0.3, 0.8)
        visible: codeVisible
        
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
                    codeVisible = false
                    enableLogin()
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
                    Widgets.TextField {
                        id: passcode
                        width: 100
                        height: 30
                        anchors.verticalCenter: parent.verticalCenter
                        onLengthChanged: {
                            if (length == 4) {
                                Poster.checkPasscode(passcode.text)
                            }
                        }
                    }
            
                    Image {
                        id: passcodeImage
                        source: Poster.passcodeUrl
                        anchors.verticalCenter: parent.verticalCenter
                        height: passcode.height - 2
                        onSourceChanged: passcode.text = ""
                    
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                Poster.newPasscode()
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
    
}