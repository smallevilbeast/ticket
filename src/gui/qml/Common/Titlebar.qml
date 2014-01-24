import QtQuick 2.1
import "../scripts/common.js" as Common
import "../Widgets" as Widgets

Item {
	id: titlebar
	
    signal closed
	function getImage (name) {
		return "qrc:/images/button/" + name + ".png"
	}
    
    Row {
        anchors.left: parent.left
        anchors.leftMargin: 5
        anchors.verticalCenter: parent.verticalCenter
        spacing: 8
        
        Image {
            source: "qrc:/images/common/logo.png"
            width: 20; height: 20
            anchors.verticalCenter: parent.verticalCenter
        }
        
        Widgets.NativeText {
            text: "抢票助手"
            anchors.verticalCenter: parent.verticalCenter
            color: "#fff"
        }
    }
	
	Row {
		id : control
		
		anchors.right: parent.right
		anchors.rightMargin: 5
				
		/* ImageButton { */
		/* 	normalImage: getImage("window_menu_normal") */
		/* 	hoverImage: getImage("window_menu_hover") */
		/* 	pressImage: getImage("window_menu_press") */
		/* } */
		
		ImageButton {
			normalImage: getImage("window_min_normal")
			hoverImage: getImage("window_min_hover")
			pressImage: getImage("window_min_press")
            onClicked: windowView.showMinimized()
		}
		
		/* ImageButton { */
		/* 	normalImage: getImage("window_max_normal") */
		/* 	hoverImage: getImage("window_max_hover") */
		/* 	pressImage: getImage("window_max_press") */
		/* } */
		
		ImageButton {
			normalImage: getImage("window_close_normal")
			hoverImage: getImage("window_close_hover")
			pressImage: getImage("window_close_press")
            onClicked: {
                titlebar.closed()
            }
		}
		
	}
	
}