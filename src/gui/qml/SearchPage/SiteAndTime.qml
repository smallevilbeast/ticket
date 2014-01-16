import QtQuick 2.1

Row {
    spacing: 5
    property alias timeText: timer.text
    property alias statusText: cross.text
    property alias stationText: site.text
    property alias font: timer.font
    property alias color: timer.color
    
    Text {
        id: timer
        text: "00:15"
    }
    
    Text {
        text: " - "
    }
    
    function getCrossColor() {
        if (cross.text == "过") {
            return "#0994bd"
        } else if (cross.text == "始") {
            return "#c65600"
        } else {
            return "#309048"
        }
    }
    
    Rectangle {
        width: cross.width + 4; height: parent.height
        color: getCrossColor()
        radius: 3
        
        Text {
            id: cross
            text: "过"
            color: "#fff"
            anchors.centerIn: parent
        }
    }
    Text {
        id: site
        text: "武昌"
    }
}
