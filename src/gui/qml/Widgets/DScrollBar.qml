import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Private 1.0


Item {
    id: container

    property variant scrollArea
    property real visibleSize: barSideMargin * 2 + barWidth
    property variant orientation: Qt.Vertical
    property bool backgroundVisible: true
    property bool inDrag: false
    property int barWidth: 6
    property int viewportWidth: scrollArea.width
    property int viewportHeight: scrollArea.height
    property int barSideMargin: 2
    opacity: 0
    Component.onCompleted: {
        layout()
    }

    WheelArea {
        id: wheelArea
        parent: scrollArea

        // ### Note this is needed due to broken mousewheel behavior in Flickable.

        anchors.fill: parent

        property int acceleration: 40
        property int flickThreshold: 20
        property real speedThreshold: 3
        property real ignored: 0.001 // ## flick() does not work with 0 yVelocity
        property int maxFlick: 400

        property bool horizontalRecursionGuard: false
        property bool verticalRecursionGuard: false

        horizontalMinimumValue: scrollArea ? scrollArea.originX : 0
        horizontalMaximumValue: scrollArea ? scrollArea.originX + scrollArea.contentWidth - viewportWidth : 0

        verticalMinimumValue: scrollArea ? scrollArea.originY : 0
        verticalMaximumValue: scrollArea ? scrollArea.originY + scrollArea.contentHeight - viewportHeight : 0

        Connections {
            target: scrollArea

            onContentYChanged: {
                wheelArea.verticalRecursionGuard = true
                wheelArea.verticalValue = scrollArea.contentY
                wheelArea.verticalRecursionGuard = false
            }
            onContentXChanged: {
                wheelArea.horizontalRecursionGuard = true
                wheelArea.horizontalValue = scrollArea.contentX
                wheelArea.horizontalRecursionGuard = false
            }
        }

        onVerticalValueChanged: {
            if (!verticalRecursionGuard) {
                if (scrollArea.contentY < flickThreshold && verticalDelta > speedThreshold) {
                    scrollArea.flick(ignored, Math.min(maxFlick, acceleration * verticalDelta))
                } else if (scrollArea.contentY > scrollArea.contentHeight
                - flickThreshold - viewportHeight && verticalDelta < -speedThreshold) {
                    scrollArea.flick(ignored, Math.max(-maxFlick, acceleration * verticalDelta))
                } else {
                    scrollArea.contentY = verticalValue
                }
            }
        }

        onHorizontalValueChanged: {
            if (!horizontalRecursionGuard)
            scrollArea.contentX = horizontalValue
        }
    }


    function layout() {
        if (container.orientation == Qt.Vertical){
            container.anchors.top = scrollArea.top
            container.anchors.bottom = scrollArea.bottom
            container.anchors.right = scrollArea.right
            container.height = scrollArea.height
            container.width = container.visibleSize

        } else {
            container.anchors.left = scrollArea.left
            container.anchors.right = scrollArea.right
            container.anchors.bottom = scrollArea.bottom
            container.height = container.visibleSize
            container.width = scrollArea.width
        }
    }

    function position()
    {
        var ny = 0;
        if (container.orientation == Qt.Vertical)
        ny = scrollArea.visibleArea.yPosition * container.height;
        else
        ny = scrollArea.visibleArea.xPosition * container.width;

        if (ny > 2) {
            return ny
        } else {
            return 2
        }
    }

    function size()
    {
        var nh, ny;

        if (inDrag) {
            return NaN
        }

        if (container.orientation == Qt.Vertical)
        nh = scrollArea.visibleArea.heightRatio * container.height;
        else
        nh = scrollArea.visibleArea.widthRatio * container.width;

        if (container.orientation == Qt.Vertical)
        ny = scrollArea.visibleArea.yPosition * container.height;
        else
        ny = scrollArea.visibleArea.xPosition * container.width;

        if (ny > 3) {
            var t;
            if (container.orientation == Qt.Vertical)
            t = Math.ceil(container.height - 3 - ny);
            else
            t = Math.ceil(container.width - 3 - ny);
            if (nh > t) return t; else return nh;

        } else return nh + ny;
    }

    function fire() {
        if (container.orientation == Qt.Vertical) {
            return scrollArea.contentHeight > scrollArea.height                            
        } else {
            return scrollArea.contentWidth > scrollArea.width            
        }
    }

    Rectangle {
        anchors.fill: parent;
        color: "white";
        opacity: 0.3; radius:5; smooth: true
        visible: container.backgroundVisible
    }

    Rectangle {
        id: scrollBorder
        radius: 6; opacity: 0.7; color: "black"
        x: container.orientation == Qt.Vertical ? barSideMargin : position()
        y: container.orientation == Qt.Vertical ? position() : barSideMargin
        width: container.orientation == Qt.Vertical ? container.barWidth: size()
        height: container.orientation == Qt.Vertical ? size() : container.barWidth
        visible: scrollArea.contentHeight > scrollArea.height || scrollArea.contentWidth > scrollArea.width 

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            drag.target: parent
            drag.axis: container.orientation == Qt.Vertical ? Drag.YAxis : Drag.XAxis
            drag.minimumX: container.x
            drag.maximumX: container.width - parent.width - container.barSideMargin
            drag.minimumY: container.y
            drag.maximumY: container.height - parent.height - container.barSideMargin
            onPressed: inDrag = true
            onReleased: inDrag = false

            onPositionChanged: {
                if (container.orientation == Qt.Vertical){
                    scrollArea.contentY = (parent.y / container.height) * scrollArea.contentHeight
                }
                else{
                    scrollArea.contentX = (parent.x / container.width) * scrollArea.contentWidth
                }

            }
        }
    }

    states: State {
        name: "visible"
        when: fire()
        PropertyChanges { target: container; opacity: 1.0 }
    }

    transitions: Transition {
        from: "visible"; to: ""
        NumberAnimation { properties: "opacity"; duration: 600 }
    }
}