# Copyright (c) 2026, Solvronix and contributors
"""Tell the desk whether to load the Pilot button, and where from. Runs once per session."""

import frappe
from frappe.utils import get_host_name


def boot_session(bootinfo):
	# Runs on every desk load: a failure here must never block ERPNext logins.
	try:
		_boot(bootinfo)
	except Exception:
		frappe.log_error(title="Pilot Connector boot failed", message=frappe.get_traceback(with_context=False))


def _boot(bootinfo):
	if frappe.session.user == "Guest" or frappe.session.data.get("user_type") != "System User":
		return
	settings = frappe.get_cached_doc("Pilot Connector Settings")
	if not settings.enabled:
		return
	allowed = {row.role for row in settings.allowed_roles}
	if allowed and not allowed & set(frappe.get_roles()):
		return
	bootinfo.pilot_connector = {
		"pilot_url": settings.pilot_url or "https://pilot.solvronix.com",
		"site": get_host_name(),
		"position": (settings.position or "Right").lower(),
	}
