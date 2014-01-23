import QtQuick 2.1
import "../Widgets" as Widgets

Component {
    Item {
        id: wrapper
        width: wrapper.ListView.view.width;
        height: 80;
        property int contentColumnSpacing: 5
        
        Component {
            id: seatComponent
            
            Row {
                property string name
                property alias num: numText.text
                spacing: 3
                function adjustColor() {
                    if (num == "有") {
                        return "green"
                    } else if (num > 0) {
                        return "#e6222a"
                    } else {
                        return "#8e8e8e"
                    }
                }
                
                function adjustTitleColor() {
                    if (num == "有" || num > 0) {
                        return "#333"
                    } else {
                        return "#8e8e8e"
                    }
                    
                }
                
                Text {
                    id: nameText;
                    text: name + ":"
                    color: adjustTitleColor()
                    font.pixelSize: 11
                }
                Text {
                    id: numText
                    color: adjustColor()
                    font.pixelSize: 11
                }
            }            
        }
        
        Component {
            id: futureComponent
            Text {
                color: "#8e8e8e"
            }
        }
                
        Rectangle {
            id: spilter
            anchors.bottom: parent.bottom
            width: parent.width; height: 1
            color: "#bcbcbc"
        }
        
        Rectangle {
            anchors.bottom: spilter.top
            width: parent.width; height: 22
            /* color: "#c7e4f8" */
            color: "#daedfa"
            
            Row {
                id: seatRow
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter                
                spacing: 20
            }
            
            Component.onCompleted: {
                if (instance.canBuy) {
                    for (var i in instance.seats) {
                        var seatObj = instance.seats[i]
                        seatComponent.createObject(seatRow, {'name': seatObj.name, 'num': seatObj.num })
                    }
                } else {
                    futureComponent.createObject(seatRow, {'text' : instance.buttonTextInfo})
                }
            }
        }
        
        Item {
            /* x: 10; y: 10 */
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 10
            anchors.leftMargin: 30
            width: parent.width; height: contentRow.height
            
            Row {
                id: contentRow
                spacing: 100
                
                Column {
                    spacing: contentColumnSpacing
                    Text {
                        text: instance.stationTrainCode
                        anchors.horizontalCenter: parent.horizontalCenter
                        /* font.pixelSize: 18 */
                        color: "#5891df"
                        font.weight: Font.Bold
                    }
                    
                    Text {
                        text: instance.lishi
                    }
                }
                
                Column {
                    spacing: contentColumnSpacing
                    SiteAndTime {
                        statusText: instance.fromStationType
                        stationText: instance.fromStationName
                        timeText: instance.startTime
                        color: "#5891df"
                        font.weight: Font.Bold
                        
                    }
                    SiteAndTime {
                        statusText: instance.toStationType
                        stationText: instance.toStationName
                        timeText: instance.arriveTime
                    }
                }
                
            }
            
            Widgets.Button {
                width: 80; height: 30
                anchors.right: parent.right                
                anchors.verticalCenter: parent.verticalCenter                
                anchors.rightMargin: 60
                text: instance.canBuy ? instance.buttonTextInfo : "抢票"
                /* onClicked: { */
                /*     Poster.test(instance) */
                /* } */

            }
            
        }
        
    }
    
}