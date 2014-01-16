import QtQuick 2.1
import QtQuick.Controls 1.0
import "../Widgets" as Widgets
import "../Common" as Common
import DGui 1.0

Item {
    width: containerRow.width; height: containerRow.height
    
    Row {
        id: containerRow
        spacing: 10
        
        Image {
            anchors.verticalCenter: parent.verticalCenter
            source: "qrc:/images/common/user_blue_add.png"
            width: 22; height: 22
            
            MouseArea {
                anchors.fill: parent
                onClicked: popupWindow.visible = true
            }
        }
        
        Repeater {
            id: displayRepeater
            anchors.verticalCenter: parent.verticalCenter
            model: Poster.selectPassengerModel()
            delegate: Component {
                Text {
                    anchors.rightMargin: 8
                    anchors.verticalCenter: displayRepeater.verticalCenter
                    text: instance.passengerName
                    color: "#1790C9"
                }
            }
        }
    }
    
    Widgets.DRectangle {
        id: popupWindow
        anchors.top: parent.bottom
        anchors.left: parent.left
        borderMargin: 10
        width: parent.width + sideWidth + 6
        height: Math.max(Math.min(titleText.height + view.contentHeight + sideWidth*2 + 10,  180+sideWidth*2),  26+sideWidth * 2)
        rectRadius: 0
        visible: false
        
        PopupItem {
            anchors.fill: parent
            windowObject: windowView
            parentObject: popupWindow
        }
        
        Item {
            anchors.fill: parent
            
            Component {
                id: passengerDelegate
                Item {
                    id: wrapper
                    width: box.width; height: box.height
                    property int code: instance.code
                    CheckBox {
                        id: box
                        text: instance.passengerName
                        onClicked: {
                            if (checked) {
                                if (displayRepeater.model.count >= 5) {
                                    checked = false
                                } else {
                                    displayRepeater.model.addPassenger(instance)
                                }
                                
                            } else {
                                displayRepeater.model.removePassenger(instance)
                            }
                        }
                    }
                }
            }
            
            Widgets.IconButton {
                source: "qrc:/images/common/refresh.png"
                anchors.right: parent.right
                anchors.top: parent.top
                iconWidth: 20; iconHeight: 20
                onClicked: Poster.requestPassengers()
            }
            
            Text {
                id: titleText
                text: "选择乘车人(最多5人)"
                font.pixelSize: 14
                color: "#1790C9"
            }
    
            Widgets.ScrollWidget {
                anchors.top: titleText.bottom
                anchors.topMargin: 10
                anchors.bottom: parent.bottom
                
                GridView {
                    id: view
                    anchors.fill: parent
                    cellWidth: 80; cellHeight: 26
                    model: Poster.passengerModel()
                    delegate: passengerDelegate
                }
            }
        }

    }
}    
