import QtQuick 2.1
import "../Common" as Common
import "../Widgets" as Widgets

Column {
    spacing: 10
    
    Row {
        spacing: 20
        Column {
            anchors.verticalCenter: parent.verticalCenter
            spacing: 5
            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "出发站"
                color: "#8e8e8e"
            }
            Widgets.CompleteInput {
                id: fromStation
                anchors.horizontalCenter: parent.horizontalCenter            
                width: 80
                model: Poster.newStationModel()
            }
        }        
            
        Common.ImageButton {
            anchors.verticalCenter: parent.verticalCenter
            normalImage: "qrc:/images/common/exchange_normal.png"
            hoverImage: "qrc:/images/common/exchange_press.png"
            pressImage: "qrc:/images/common/exchange_press.png"
            onClicked: {
                var fromText = fromStation.text
                var toText = toStation.text
                var fromTelecode = fromStation.telecode
                var toTelecode = toStation.telecode
                fromStation.setName(toText)
                toStation.setName(fromText)
                fromStation.telecode = toTelecode
                toStation.telecode = fromTelecode
            }
        }
            
        Column {
            anchors.verticalCenter: parent.verticalCenter
            spacing: 5
            Text {
                anchors.horizontalCenter: parent.horizontalCenter            
                text: "出发站"
                color: "#8e8e8e"
            }
            Widgets.CompleteInput {
                id: toStation
                anchors.horizontalCenter: parent.horizontalCenter            
                width: 80
                model: Poster.newStationModel()
            }
        }        
        z: 1000
    }
    
    Row {
        spacing: 10
        Text { text: "日期"; anchors.verticalCenter: parent.verticalCenter; font.pixelSize: 14 }
        Widgets.Calendar { id: calendar; anchors.verticalCenter: parent.verticalCenter; width: 210}
    }
    
    PassengerView {
        width: 250
        z: 800
    }
    
    SeatView {
        width: 250
        z: 700
    }
    
    Widgets.TextField {
        width: 250
        Keys.onReturnPressed: {
            Poster.submitTickets(text)
        }
    }

    Widgets.Button {
        text: "查询"
        width: 250; height: 36
        onClicked: Poster.queryTrains(fromStation.telecode, toStation.telecode, calendar.text)
    }
    
}
