import QtQuick 2.1
import QtGraphicalEffects 1.0

Item {
	
	Item {
        id: container;
        anchors.centerIn: parent;
        width:  parent.width - rectShadow.radius * 2
        height: parent.height - rectShadow.radius * 2

        Rectangle {
            id: rect
            width: parent.width
            height: parent.height
			color: Qt.rgba(49/255.0, 8/255.0, 97/255.0, 0.10)
            radius: 3;
            antialiasing: true;
            border {
                width: 1;
                color: Qt.rgba(0, 0, 0, 0.2);
            }
            anchors.centerIn: parent;
        }
    }
	
	DropShadow {
		id: rectShadow;
		anchors.fill: container
		cached: true
		horizontalOffset: -2
		verticalOffset: 2
		radius: 3.0
		samples: 16
		color: "#ffffff"
		smooth: true
		source: container
	}
}
