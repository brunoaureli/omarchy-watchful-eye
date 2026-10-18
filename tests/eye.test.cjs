const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');

const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const eye = {};
vm.createContext(eye);
vm.runInContext(read('Eye.js').replace(/^\.pragma library\s*/, ''), eye);

test('all gaze directions retain a fixed block-only character grid', () => {
  for (const x of [-1, -0.5, 0, 0.5, 1]) {
    for (const y of [-1, 0, 1]) {
      const frame = eye.render(x, y);
      assert.equal(frame.split('\n').length, eye.rows);
      assert(frame.split('\n').every(row => row.length === eye.columns));
      assert.match(frame, /█/u);
      assert.doesNotMatch(frame, /[^ ▀▄░▒▓█\n]/u);
    }
  }
});

test('the dark pupil follows horizontal and vertical gaze, not just the texture', () => {
  function pupilCenter(frame) {
    const points = [];
    frame.split('\n').forEach((line, y) => [...line].forEach((char, x) => {
      // The central opening has no blank cells except the moving pupil.
      if (char === ' ' && x >= 20 && x <= 70 && y >= 9 && y <= 14) points.push([x, y]);
    }));
    assert(points.length > 0);
    return points.reduce((sum, point) => [sum[0] + point[0] / points.length, sum[1] + point[1] / points.length], [0, 0]);
  }
  assert(pupilCenter(eye.render(-1, 0))[0] < pupilCenter(eye.render(1, 0))[0]);
  assert(pupilCenter(eye.render(0, -1))[1] < pupilCenter(eye.render(0, 1))[1]);
  assert.equal(eye.render(100, -100), eye.render(1, -1));
});

test('out-of-eye pixels stay empty at every gaze extreme', () => {
  for (const gaze of [[-1, -1], [-1, 1], [1, -1], [1, 1]]) {
    const lines = eye.render(...gaze).split('\n');
    for (let row = 0; row < eye.rows; row++) {
      for (let x = 0; x < eye.columns; x++) {
        if (eye.opening(x) < 0 ||
            (Math.abs(row * 2 - eye.middleY) > eye.opening(x) + 1.3 &&
             Math.abs(row * 2 + 1 - eye.middleY) > eye.opening(x) + 1.3)) {
          assert.equal(lines[row][x], ' ');
        }
      }
    }
  }
});

test('authentication code retains the tested stock Omarchy implementation', () => {
  const service = read('Service.qml');
  const baseline = JSON.parse(read('upstream/authentication.json'));
  const authentication = service.split('  PanelWindow {', 1)[0] + '\n' + service.split('  PamContext {').slice(1).join('  PamContext {');
  assert.equal(crypto.createHash('sha256').update(authentication).digest('hex'), baseline.sha256);
});

test('preview is visibly labeled, read-only and has no password submission handler', () => {
  const preview = read('Service.qml').split('  PanelWindow {')[1].split('  PamContext {')[0];
  assert.match(preview, /inputEnabled: false/);
  assert.match(preview, /passwordText: ""/);
  assert.match(preview, /PREVIEW/);
  assert.match(preview, /Keys\.onEscapePressed/);
  assert.doesNotMatch(preview, /onSubmitPassword|onPasswordTextEdited|demoPassword/);
});

test('the public manifest replaces the built-in lock and includes attribution', () => {
  const manifest = JSON.parse(read('manifest.json'));
  assert.equal(manifest.id, 'io.github.brunoaureli.watchful-eye');
  assert.equal(manifest.omarchy.clonedFrom, 'omarchy.lock');
  assert(manifest.omarchy.capabilities.includes('authentication'));
  for (const entry of Object.values(manifest.entryPoints)) assert(fs.existsSync(path.join(root, entry)));
  assert.match(read('LICENSE'), /David Heinemeier Hansson/);
});
