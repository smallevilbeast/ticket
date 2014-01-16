import QtQuick 2.1
 
Text {
    id: textItem
 
    property real minWidth: 0
    property real maxWidth: 10000
 
    property real minHeight: 0
    property real maxHeight: 10000
 
    property real dynamicWidth: 0
    property real dynamicHeight: 0
 
 
    function updateWidth(){
 
        dynamicWidth = widthComputingWorkaround.paintedWidth
 
        if( dynamicWidth > maxWidth ){
            dynamicWidth = maxWidth
        }
        if( dynamicWidth < minWidth ){
            dynamicWidth = minWidth
        }
        if( dynamicWidth < 0 ){
            dynamicWidth = 0
        }
 
        dynamicHeight = widthComputingWorkaround.paintedHeight
 
        if( dynamicHeight > maxHeight ){
            dynamicHeight = maxHeight
        }
        if( dynamicHeight < minHeight ){
            dynamicHeight = minHeight
        }
        if( dynamicHeight < 0 ){
            dynamicHeight = 0
        }
    }
 
    width: dynamicWidth
    height: dynamicHeight
 
    Text {
        id: widthComputingWorkaround
        text: textItem.text
        font: textItem.font
        textFormat: textItem.textFormat
        opacity: 0
 
        // this has to be called here, because textItem sends them before the workaround notices it,
        // which leads to wrong dimensions.
        onTextChanged: updateWidth()
        onFontChanged: updateWidth()
    }
 
    onMinWidthChanged: updateWidth()
    onMaxWidthChanged: updateWidth()
    onMinHeightChanged: updateWidth()
    onMaxHeightChanged: updateWidth()
    Component.onCompleted: updateWidth()
}