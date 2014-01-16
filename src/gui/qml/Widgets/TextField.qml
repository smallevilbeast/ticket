import QtQuick 2.1
import QtQuick.Controls 1.0
import "../Styles" as Styles

TextField {
    width: 160; height: 30
    property int radius: 3
    style: Styles.TextFieldStyle {}
    font.pixelSize: 14
}