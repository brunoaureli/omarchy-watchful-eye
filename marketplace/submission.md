### Repository URL

https://github.com/brunoaureli/omarchy-watchful-eye

### Category

Appearance

### Tags

hyprland, quickshell, security

### Suggest a missing tag

_No response_

### Maintainer notes

Watchful Eye 0.1.0 replaces the Omarchy lock service using the documented clone
mechanism (`omarchy.clonedFrom: omarchy.lock`). It declares the authentication
capability. This is intentionally submitted as authentication-capable code.

The password/fingerprint PAM flows and lock lifecycle match the stock Omarchy
4.0.4-1 service byte for byte, excluding only the read-only visual preview window.
The repository includes an authentication-section digest, a complete upstream
service digest, attribution, a compatibility-check helper, and an explanation of
the copied upstream baseline. The preview is explicitly labeled, read-only and
does not attempt authentication.

Validated locally with Omarchy's manifest validator, Node renderer/contract tests,
and an offscreen Qt interaction test covering preview/lock-view pointer movement,
masked typing, Enter submission handoff, and Ctrl+U. The interaction test does not
start a lock service or call PAM. Real Wayland lock acquisition, PAM success,
fingerprint hardware, multi-monitor and suspend/resume are not covered by those
headless tests. Compatibility is currently advertised only for Omarchy 4.0.4.

The plugin has no installation script, network fetches or additional runtime
dependencies. Configuration changes happen through Omarchy's explicit enable and
disable commands. The original block artwork and synthetic-input preview are
submitted by their owner; the Omarchy-derived files retain MIT attribution.

### Submission checklist

- [x] The repository is public and contains installation and removal instructions.
- [x] I have documented the plugin license and any external dependencies.
- [x] I confirm that I own or have permission to submit this plugin and its preview assets.
- [x] The plugin does not overwrite user configuration without explicit consent.
- [x] I understand that approval is for listing and is not a security review.
