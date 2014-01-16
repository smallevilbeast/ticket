import QtQuick 2.1
import "../Widgets" as Widgets

Item {
    SearchForm {
        anchors.top: parent.top
        anchors.topMargin: 40
        id: searchForm
        
        anchors.horizontalCenter: parent.horizontalCenter
        z: 100
    }
    
    Widgets.ScrollWidget {
        anchors.top: searchForm.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 10
        width: parent.width

        ListView {
            id: resultView
            anchors.fill: parent
            model: Poster.trainModel()
            delegate: SiteDelegate {}
            clip: true
        }

    }
}
