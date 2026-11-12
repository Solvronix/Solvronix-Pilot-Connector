# Copyright (c) 2026, Solvronix and contributors
"""Tell the desk whether to load the Pilot button, and which Pilot server the chat panel
opens from. Runs once per session."""

import frappe
from frappe.utils import get_host_name

from solvronix_pilot_connector import __version__


def boot_session(bootinfo):
	# Runs on every desk load: a failure here must never block ERPNext logins.
	try:
		_boot(bootinfo)
	except Exception:
		frappe.log_error(title="Pilot Connector boot failed", message=frappe.get_traceback(with_context=False))


def _boot(bootinfo):
	cfg = button_config()
	if cfg:
		bootinfo.pilot_connector = cfg


def button_config() -> dict | None:
	"""The Pilot button for the current user, or None when they should not see it.
	Used at desk load (boot) and again when the settings change (api.button_config)."""
	if frappe.session.user == "Guest" or frappe.session.data.get("user_type") != "System User":
		return None
	settings = frappe.get_cached_doc("Pilot Connector Settings")
	if not settings.enabled:
		return None
	allowed = {row.role for row in settings.allowed_roles}
	if allowed and not allowed & set(frappe.get_roles()):
		return None
	return {
		"pilot_url": settings.pilot_url or "https://pilot.solvronix.com",
		"site": get_host_name(),
		"position": (settings.position or "Right").lower(),
		# Cache key for the bundled button script: changes with every connector release.
		"version": __version__,
	}
