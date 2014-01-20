import QtQuick 2.1


TextField {
    readOnly: true    
    property bool clickFlag: false
    radius: 0
    signal calendarChanged(string date)
    signal calendarClicked(var date)
    
    Component.onCompleted: {
        windowView.calendarChanged.connect(calendarChanged)
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
    
    onCalendarChanged: {
        text = date
        clickFlag = false
    }
}