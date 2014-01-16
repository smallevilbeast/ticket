import QtQuick 2.1


TextField {
    readOnly: true    
    property bool clickFlag: false
    radius: 0
    signal calendarClicked(string date)
    
    Component.onCompleted: {
        windowView.calendarClicked.connect(calendarClicked)
        text = windowView.today()
    }
    
    MouseArea {
        anchors.fill: parent
        onClicked: {
            clickFlag = true
            var pos =  parent.mapToItem(null, 0, parent.height)
            windowView.showCalendar(pos.x, pos.y)
        }
        cursorShape: Qt.PointingHandCursor
    }
    
    onCalendarClicked: {
        if (clickFlag) {
            text = date
            clickFlag = false
        }
    }
}