# Changelog

All notable changes to the Solvronix Pilot Connector. Versions follow [Semantic Versioning](https://semver.org/). Frappe Cloud and the install steps use the `version-16` branch, which always points at the latest tested release.

## [0.1.6] — 2026-11-11 — Ready for the Frappe Cloud Marketplace

### Changed
- `pyproject.toml` now states the supported Frappe versions (`[tool.bench.frappe-dependencies]`: Frappe 16) and the repository link, as the Frappe Cloud Marketplace requires. No change to how the app works.

## [0.1.5] — 2026-11-11 — Phone alerts without setup

ERPNext alerts reach your team's phones with one tick in the Pilot console. There's no Webhook, no secret key and no JSON to set up.

### Added
- **Phone alerts.** When phone notifications are on in the Pilot console, the connector tells Pilot about each new ERPNext notification (the bell): only its name and its recipient. Pilot reads the alert back with that person's own login, so nothing can be faked. People who haven't turned on alerts on a phone are never involved. Nothing is sent while alerts are off for your site. The connector checks this at most every 10 minutes.
- **Short address.** `your-erpnext-address/pilot` opens Pilot for your company. That's handy on phones, where people only need to remember their own ERPNext address.

### Changed
- An ERPNext save never waits for Pilot or fails because of it: alerts are sent in the background, after the save is complete.

## [0.1.4] — 2026-11-11 — Button ships inside the app

### Changed
- **The button's code now ships inside the app.** No script from another server runs in your ERPNext. Only the chat panel opens from Pilot, in a separate frame that cannot read or change the ERPNext page around it.
- The button's cache key changes with every release, so browsers pick up a new button right away.
- Supports Python 3.10 and later.

### Fixed
- Fresh installs work straight away: Pilot Connector Settings are saved with their defaults on install. Before this, a new install could show the button while Pilot's console reported the connector as switched off.
- The health check Pilot uses ("Installed" in the owner console) reads the same settings as the button.

## [0.1.2] — 2026-11-06 — Install steps and tests

### Added
- Install, update and uninstall steps in the README.
- First automated tests (health check, settings validation, button role rules).

## [0.1.1] — 2026-11-06 — First release

### Added
- The **Ask Pilot** button on every ERPNext desk page.
- **Pilot Connector Settings**: on/off, button position, Pilot address, and which roles see the button.
- A read-only health check, so Pilot's owner console can show "Installed".

## [0.0.1] — 2026-10-23
- App created.
