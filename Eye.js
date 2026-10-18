.pragma library

var columns = 91
var rows = 25
var middleX = 45
var middleY = 24

function opening(x) {
  var dx = (x - middleX) / 42
  return Math.abs(dx) <= 1 ? 13 * Math.pow(Math.max(0, 1 - dx * dx), 0.72) : -1
}

function pixel(x, y, cx, cy) {
  var lid = opening(x)
  var height = Math.abs(y - middleY)
  if (lid < 0 || height > lid + 1.3) return 0
  // Thick upper and lower lids. Two vertical pixels share one block character.
  if (height > lid - 1.4) return 1
  var dx = x - cx, dy = y - cy
  var radius = Math.sqrt(dx * dx + dy * dy)
  if (radius <= 12.4) {
    // A dark pupil and bright reflection make the lens read as an eye.
    if ((dx + 3) * (dx + 3) + (dy + 4) * (dy + 4) < 4) return 1
    if (radius < 4.5) return 0
    if (radius < 5.7) return 0.95
    if (radius > 11) return 0.95
    var angle = Math.atan2(dy, dx)
    return 0.38 + 0.48 * Math.pow(Math.abs(Math.sin(angle * 14 + radius * 0.45)), 1.3)
  }
  // Quiet sclera; shade toward the corners and the upper lid.
  return height > lid - 4 ? 0.22 : 0.36
}

function block(top, bottom) {
  if (top === 0 && bottom === 0) return " "
  if (top === 0) return "▄"
  if (bottom === 0) return "▀"
  var intensity = (top + bottom) / 2
  return intensity > 0.88 ? "█" : intensity > 0.6 ? "▓" : intensity > 0.3 ? "▒" : "░"
}

function render(gazeX, gazeY) {
  var cx = middleX + Math.round(Math.max(-1, Math.min(1, gazeX || 0)) * 18)
  var cy = middleY + Math.round(Math.max(-1, Math.min(1, gazeY || 0)) * 3)
  var lines = []
  for (var row = 0; row < rows; row++) {
    var line = ""
    for (var x = 0; x < columns; x++) line += block(pixel(x, row * 2, cx, cy), pixel(x, row * 2 + 1, cx, cy))
    lines.push(line)
  }
  return lines.join("\n")
}

function template() { return render(0, 0) }
