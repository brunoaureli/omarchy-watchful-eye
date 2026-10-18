# Upstream baseline

Watchful Eye 0.1.0 was built against Omarchy package `4.0.4-1`.

Source: https://github.com/omacom/omarchy

Upstream files:

- `shell/plugins/lock/Service.qml`: authentication and session-lock service.
- `shell/plugins/lock/LockView.qml`: password entry and base presentation.

These files are MIT licensed, copyright David Heinemeier Hansson. The root
LICENSE retains that attribution alongside the new artwork's attribution.

`upstream/Service.qml.sha256` records the exact installed stock-service file used
as the baseline. `watchful-eye check` compares the target system against it.

`upstream/authentication.json` records a SHA-256 digest of the stock service with
only its preview `PanelWindow` removed. The Node test verifies that this package
preserves those authentication and lock-lifecycle sections byte for byte.

The preview-only differences are pointer-coordinate forwarding, a PREVIEW label
and Escape dismissal. The preview remains non-authenticating and read-only.

When porting to a newer Omarchy version, review the complete upstream lock-service
diff, update the snapshot and both baselines, rerun tests, and perform a real lock
and unlock test before advertising compatibility. Passing a digest check does
not by itself verify PAM behavior or the compositor's lock implementation.
