import QtQuick 2.1
import "../Widgets" as Widgets

Item {
    id: root
    signal clicked
    property bool codeVisible: false
    
    Connections {
        target: Poster
        onGrabTicketsSuccessed: {
            displayColumn.visible = false
            notifyColumn.visible = true
        }
    }
    
    Column {
        id: notifyColumn
        anchors.centerIn: parent        
        spacing: 20
        visible: false
        
        Widgets.NativeText {
            text: "恭喜你抢票成功!, 请稍后登录12306查询订单"
            font.pixelSize: 16
        }
        
        Widgets.Button {
            text: "重新抢票"
            width: 250; height: 36
            onClicked: {
                notifyColumn.visible = false
                displayColumn.visible = !codeVisible
                Poster.grabTicketFlag = false
                root.clicked()
            }
        }
        
    }
    
    Column {
        id: displayColumn
        spacing: 20
        visible: !codeVisible
        anchors.centerIn: parent        
        
        Widgets.NativeText {
            text: "正在刷票..."
            font.pixelSize: 14
            font.weight: Font.Bold
        }
        
        Row {
            Widgets.NativeText { text: "已尝试 "; anchors.verticalCenter: parent.verticalCenter }
            Widgets.NativeText { text: Poster.queryNumber; color: "#FDA231"; font.pixelSize: 18; anchors.verticalCenter: parent.verticalCenter  }
            Widgets.NativeText { text: " 次, "; anchors.verticalCenter: parent.verticalCenter }
            Widgets.NativeText { text: Poster.queryRemainingTime; color: "#FDA231"; font.pixelSize: 18; anchors.verticalCenter: parent.verticalCenter  }
            Widgets.NativeText { text: " 秒后继续尝试"; anchors.verticalCenter: parent.verticalCenter }
        }
        
        Widgets.Button {
            text: "停止抢票"
            width: 250; height: 36
            onClicked: {
                Poster.grabTicketFlag = false
                root.clicked()
            }
        }
        
    }
    
    Widgets.Passcode {
        anchors.fill: parent
        module: "passenger"
        visible: codeVisible
        onCloseClicked: {
            codeVisible = false
        }
        onPasscodeUpdated: {
            codeVisible = true
            codeFocus = true
        }
        onPasscodeSuccessed: {
            codeVisible = false
            Poster.submitTickets(text)
        }
        
    }
    
}