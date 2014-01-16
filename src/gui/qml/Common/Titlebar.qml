import QtQuick 2.1
import "../scripts/common.js" as Common

Item {
	id: titlebar
	
    signal closed
	function getImage (name) {
		return "qrc:/images/button/" + name + ".png"
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
		}
		
		ImageButton {
			normalImage: getImage("window_max_normal")
			hoverImage: getImage("window_max_hover")
			pressImage: getImage("window_max_press")
		}
		
		ImageButton {
			normalImage: getImage("window_close_normal")
			hoverImage: getImage("window_close_hover")
			pressImage: getImage("window_close_press")
            onClicked: {
                /* Common.findParent(titlebar).destroy() */
                titlebar.closed()
            }
		}
		
	}
	
}