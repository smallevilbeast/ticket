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
        
        Widgets.AddButton {
            onClicked: popupWindow.visible = true
        }
        
        Repeater {
            id: displayRepeater
            anchors.verticalCenter: parent.verticalCenter
            model: Poster.selectSeatModel()
            delegate: Component {
                Widgets.NativeText {
                    anchors.rightMargin: 8
                    anchors.verticalCenter: displayRepeater.verticalCenter
                    text: instance.seatName
                    color: "#1790C9"
                }
            }
        }
    }
    
    Widgets.DRectangle {
        id: popupWindow
        anchors.top: parent.bottom
        anchors.left: parent.left
        anchors.leftMargin: -10
        anchors.topMargin: -8
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
                id: seatDelegate
                Item {
                    id: wrapper
                    width: box.width; height: box.height
                    CheckBox {
                        id: box
                        text: instance.seatName
                        onClicked: {
                            if (checked) {
                                if (displayRepeater.model.count >= 5) {
                                    checked = false
                                } else {
                                    displayRepeater.model.addObj(instance)
                                }
                                
                            } else {
                                displayRepeater.model.removeObj(instance)
                            }
                        }
                    }
                }
            }

            Widgets.NativeText {
                id: titleText
                text: "选择期望席别(按优先级,最多5人)"
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
                    model: Poster.seatModel()
                    delegate: seatDelegate
                }
            }
        }

    }
}    
