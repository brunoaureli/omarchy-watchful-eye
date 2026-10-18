#!/usr/bin/env python3
"""Offscreen presentation/input test. Never launches Service.qml or calls PAM."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', type=Path, help='save a synthetic-input screenshot')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    stock = Path(os.environ.get('OMARCHY_PATH', '/usr/share/omarchy')) / 'shell'
    if not shutil.which('qs') or not (stock / 'Ui').is_dir():
        parser.error('Quickshell and the installed Omarchy shell modules are required')
    target = str(args.preview.resolve()) if args.preview else ''
    with tempfile.TemporaryDirectory(prefix='watchful-eye-test-') as directory:
        root = Path(directory)
        runtime = root / 'runtime'
        runtime.mkdir(mode=0o700)
        home = root / 'home'
        theme = home / '.local/state/omarchy/current/theme'
        theme.mkdir(parents=True)
        (theme / 'colors.toml').write_text('background = "#05080a"\nforeground = "#fff6ff"\naccent = "#b2fff3"\n')
        for source in stock.iterdir():
            if source.is_dir():
                (root / source.name).symlink_to(source, target_is_directory=True)
        qml = '''import QtQuick
import QtQuick.Window
import QtTest
import __PLUGIN__ as Lock
Window {
  id: window
  visible: true
  width: 1280; height: 720
  property string entered: ""
  property string submitted: ""
  property int stage: 0
  Lock.LockView {
    id: view
    anchors.fill: parent
    loadBackground: false
    inputEnabled: !previewOverlay.visible
    passwordText: window.entered
    onPasswordTextEdited: function(password) { window.entered = password }
    onSubmitPassword: function(password) { window.submitted = password }
  }
  MouseArea {
    id: previewOverlay
    anchors.fill: parent
    hoverEnabled: true
    onPositionChanged: function(mouse) { view.trackPointer(mouse.x, mouse.y) }
  }
  TestCase { id: events; name: "WatchfulEyeInteraction"; when: false }
  function find(item, predicate) {
    if (predicate(item)) return item
    var children = item.children || []
    for (var i = 0; i < children.length; i++) {
      var match = find(children[i], predicate)
      if (match) return match
    }
    return null
  }
  function fail(code, message) { console.error(message); Qt.exit(code) }
  Timer {
    interval: 300; running: true; repeat: true
    onTriggered: {
      var eye = find(view, function(item) { return "frameText" in item })
      var field = find(view, function(item) { return "borderSpec" in item && item.width === 381 })
      var input = find(view, function(item) { return "passwordCharacter" in item })
      if (!eye || !field || !input || field.color.a !== 0 || field.borderTop !== 0 || view.placeholderText !== "") {
        fail(1, "Missing presentation or non-empty password chrome"); return
      }
      if (stage === 0) {
        events.mouseMove(view, 120, 220)
      } else if (stage === 1) {
        if (eye.gazeX >= 0 || !view.pointerSeen) { fail(2, "Preview gaze did not move left"); return }
        events.mouseMove(view, 1160, 220)
      } else if (stage === 2) {
        if (eye.gazeX <= 0) { fail(3, "Preview gaze did not move right"); return }
        previewOverlay.visible = false
        events.mouseMove(view, 180, 220)
      } else if (stage === 3) {
        if (eye.gazeX >= 0 || view.pointerX !== 180) { fail(4, "Lock-view gaze did not follow pointer"); return }
        input.forceActiveFocus()
        for (var i = 0; i < 6; i++) events.keyClick(Qt.Key_A)
      } else if (stage === 4) {
        if (input.displayText !== "●●●●●●" || window.entered !== "aaaaaa") { fail(5, "Masked typing failed"); return }
        events.keyClick(Qt.Key_Return)
      } else if (stage === 5) {
        if (window.submitted !== "aaaaaa" || window.entered !== "") { fail(6, "Enter submission handoff failed"); return }
        events.keyClick(Qt.Key_B)
        events.keyClick(Qt.Key_U, Qt.ControlModifier)
      } else if (stage === 6) {
        if (window.entered !== "" || input.displayText !== "") { fail(7, "Ctrl+U did not clear the field"); return }
        for (var j = 0; j < 6; j++) events.keyClick(Qt.Key_A)
        view.trackPointer(view.width / 2, view.height * 0.4)
      } else {
        stop()
        var output = __OUTPUT__
        if (output) view.grabToImage(function(result) { Qt.exit(result.saveToFile(output) ? 42 : 8) })
        else Qt.exit(42)
      }
      stage++
    }
  }
}
'''.replace('__PLUGIN__', json.dumps(repo.as_uri())).replace('__OUTPUT__', json.dumps(target))
        (root / 'shell.qml').write_text(qml)
        environment = dict(os.environ,
            HOME=str(home), XDG_CONFIG_HOME=str(home / '.config'),
            XDG_DATA_HOME=str(home / '.local/share'), XDG_STATE_HOME=str(home / '.local/state'),
            XDG_CACHE_HOME=str(root / 'cache'), XDG_RUNTIME_DIR=str(runtime),
            QT_QPA_PLATFORM='offscreen', QT_QPA_PLATFORMTHEME='', QT_QUICK_BACKEND='software',
            QT_QUICK_CONTROLS_STYLE='Basic', QML_DISK_CACHE_PATH=str(root / 'qml-cache'),
            QT_FORCE_STDERR_LOGGING='1', QT_LOGGING_TO_CONSOLE='1')
        environment.pop('WAYLAND_DISPLAY', None)
        result = subprocess.run(['qs', '--no-color', '-p', str(root)], env=environment,
                                capture_output=True, text=True, timeout=15)
        if result.returncode != 42:
            print(result.stdout + result.stderr)
            raise SystemExit(f'Interaction test failed (exit {result.returncode})')
    print('PASS: preview and lock-view pointer tracking, invisible idle field, masked typing, Enter handoff, Ctrl+U.')
    if target:
        print('Screenshot:', target)


if __name__ == '__main__':
    main()
