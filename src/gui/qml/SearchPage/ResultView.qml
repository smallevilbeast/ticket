import QtQuick 2.1
import "../Widgets" as Widgets
import "../Common" as Common

Item {
    signal backClicked
    Rectangle {
        id: topBar
        anchors.top: parent.top
        anchors.topMargin: -1
        width: parent.width
        height: 50
        color: Qt.rgba(51/255.0, 51/255.0, 51/255.0, 0.6)
        
        Common.ImageButton {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            normalImage: "qrc:/images/common/back_normal.png"
            hoverImage: "qrc:/images/common/back_press.png"
            pressImage: "qrc:/images/common/back_press.png"
            onClicked: backClicked()
        }
        
        Widgets.Button {
            anchors.left: parent.left
            anchors.leftMargin: 50
            anchors.verticalCenter: parent.verticalCenter
            width: 80; height: 26
            text: "前一天"
            onClicked: Poster.queryTrainModel().previousDay()
        }    
        
        Widgets.Calendar {
            id: calendar
            width: 100; height: 26
            anchors.centerIn: parent            
            textColor: "#fff"
            onCalendarClicked: {
                Poster.queryTrainModel().queryByDate(date)
            }
        }
        
        Widgets.Button {
            anchors.right: parent.right
            anchors.rightMargin: 30
            anchors.verticalCenter: parent.verticalCenter
            width: 80; height: 26
            text: "后一天"
            onClicked: Poster.queryTrainModel().nextDay()
        }    
    }
    
    Widgets.ScrollWidget {
        anchors.top: topBar.bottom
        anchors.bottom: parent.bottom
        rightMargin: 2
        width: parent.width
        
        ListView {
            id: resultView
            anchors.fill: parent
            model: Poster.queryTrainModel()
            delegate: SiteDelegate {}
            clip: true
        }
    }
}
