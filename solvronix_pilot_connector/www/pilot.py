# Copyright (c) 2026, Solvronix and contributors
"""yourerp.com/pilot: a short address for Pilot. Opens Pilot already set to this ERPNext,
so on a phone people only need to remember their own ERPNext address."""

from urllib.parse import quote

import frappe
from frappe.utils import get_host_name

no_cache = 1


def get_context(context):
	settings = frappe.get_cached_doc("Pilot Connector Settings")
	if not settings.enabled:
		context.title = "Solvronix Pilot"
		return context
	base = (settings.pilot_url or "https://pilot.solvronix.com").rstrip("/")
	frappe.local.flags.redirect_location = f"{base}/pilot?site={quote(get_host_name())}"
	# 302, not the default 301: browsers must not remember it (the address or switch may change).
	raise frappe.Redirect(302)
