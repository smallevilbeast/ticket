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
                url: "https://kyfw.12306.cn/otn/regist/init"
                renderType: Text.NativeRendering                
            }

        }
        
        Widgets.Button {
            id: loginButton
            width: columnWidth; height: columnHeight
            text: "登录"
            onClicked: checkLogin()
        }
        
    }
    
    Widgets.Passcode {
        id: passcode
        anchors.fill: parent
        visible: codeVisible
        module: "login"
        onCloseClicked: {
            codeVisible = false
            enableLogin()
        }
        
        onPasscodeUpdated: {
            codeVisible = true
            codeFocus = true
        }
        onPasscodeSuccessed: {
            codeVisible = false
            Poster.login(passcode.text)
        }
    }
}