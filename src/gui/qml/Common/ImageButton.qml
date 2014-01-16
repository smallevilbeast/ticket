import QtQuick 2.1


Item {
	id: root
	
	width: image.width;	height: image.height    
	property string normalImage
	property string hoverImage
	property string pressImage
	signal clicked
    
	Image {
		id: image
		source: normalImage
	}
	
	MouseArea {
		id: mouseArea
		anchors.fill: root
		hoverEnabled: true
		onEntered: { image.source = hoverImage }
		onExited: { image.source = normalImage }
		onPressed: { image.source = pressImage }
		onReleased: { image.source= mouseArea.containsMouse ? hoverImage : normalImage}
		onClicked: {
            root.clicked()
        }
	}
}