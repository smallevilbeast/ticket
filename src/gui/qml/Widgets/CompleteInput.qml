import QtQuick 2.1
import DGui 1.0

TextField {
    id: container
    radius: 0
    focus: true
    property var model: 5
    property bool manualFlag: false
    property string telecode
    onFocusChanged: {
        if (!focus) {
            popupWindow.visible = false
        }
    }
    
    Connections {
        target: model
        onCountChanged: {
            if (model.count > 0)  {
                popupWindow.visible = true
            } else {
                popupWindow.visible = false
            }
        }
    }

    Component {
        id: wrapperComponent
        Item {
            id: wrapper
            width: wrapper.ListView.view.width; height: 26
            
            Rectangle {
                color: wrapper.ListView.view.currentIndex == index ? "#1790C9" : "#fff"
                anchors.fill: parent
            }

            Text {
                anchors.left: parent.left
                anchors.leftMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                text: instance.name
                color: wrapper.ListView.view.currentIndex == index ? "#fff" : "#000"
            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                hoverEnabled: true
                onContainsMouseChanged: {
                    if (containsMouse && wrapper.ListView.view.currentIndex != index) {
                        wrapper.ListView.view.currentIndex = index
                    }
                }
                onClicked: setNameFromView()
                
            }
        }
    }
    
    function setNameFromView() {
        var obj = container.model.get(completeView.currentIndex)
        setName(obj.name)
        telecode = obj.telecode
        popupWindow.visible = false
    }
    
    function setName(value) {
        manualFlag = true        
        container.text = value
        manualFlag = false
    }

    Keys.onDownPressed: {
        completeView.incrementCurrentIndex()
    }
    Keys.onUpPressed: {
        completeView.decrementCurrentIndex()
    }
    Keys.onReturnPressed: setNameFromView()        
    
    onLengthChanged: {
        if (!manualFlag) {
            model.complete(text)
            completeView.currentIndex = 0
        }
    }
    
    DRectangle {
        id: popupWindow
        anchors.top: parent.bottom
        anchors.left: parent.left
        borderMargin: 2            
        anchors.leftMargin: -sideWidth + 3
        anchors.topMargin: -sideWidth / 2 - 3
        width: parent.width + sideWidth + 6
        height: Math.max(Math.min(completeView.contentHeight + sideWidth*2,  180+sideWidth*2),  26+sideWidth * 2)
        rectRadius: 0
        visible: false
        
        PopupItem {
            anchors.fill: parent
            windowObject: windowView
            parentObject: popupWindow
        }
        
        Item {
            anchors.fill: parent

            ScrollWidget {
                anchors.fill: parent
                ListView {
                    id: completeView                    
                    anchors.fill: parent
                    model: container.model
                    delegate: wrapperComponent
                    clip: true
                    interactive: false
                }
            }
        }

    }
}

