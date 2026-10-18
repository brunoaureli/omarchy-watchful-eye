import QtQuick
import "Eye.js" as Eye

Item {
  id: root

  property color foreground: "#fff6ff"
  property real pointerX: width / 2
  property real pointerY: height / 2
  property real lookRangeX: 500
  property real lookRangeY: 300
  property real gazeX: Math.max(-1, Math.min(1, (pointerX - width / 2) / Math.max(1, lookRangeX)))
  property real gazeY: Math.max(-1, Math.min(1, (pointerY - height / 2) / Math.max(1, lookRangeY)))
  readonly property string frameText: Eye.render(gazeX, gazeY)

  implicitWidth: 880
  implicitHeight: 300

  TextMetrics {
    id: baseCell
    font.family: "monospace"
    font.pixelSize: 24
    text: "M"
  }
  FontMetrics {
    id: baseFont
    font.family: "monospace"
    font.pixelSize: 24
  }
  TextMetrics {
    id: actualCell
    font: eyeText.font
    text: "M"
  }

  // Character-cell motion with a short ease: no continuously running timer.
  Behavior on gazeX { NumberAnimation { duration: 140; easing.type: Easing.OutCubic } }
  Behavior on gazeY { NumberAnimation { duration: 140; easing.type: Easing.OutCubic } }

  Text {
    id: eyeText
    anchors.centerIn: parent
    width: actualCell.advanceWidth * Eye.columns
    text: root.frameText
    textFormat: Text.PlainText
    color: root.foreground
    font.family: "monospace"
    font.weight: Font.Medium
    font.pixelSize: Math.max(6, Math.floor(Math.min(24,
      root.width * 24 / (Eye.columns * baseCell.advanceWidth),
      root.height * 24 / (Eye.rows * baseFont.lineSpacing))))
    font.kerning: false
    // Center the fixed grid as a whole; centering individual lines distorts ASCII.
    horizontalAlignment: Text.AlignLeft
    wrapMode: Text.NoWrap
  }
}
