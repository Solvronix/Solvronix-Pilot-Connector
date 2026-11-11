# Copyright (c) 2026, Solvronix and contributors
import frappe

from solvronix_pilot_connector import __version__


@frappe.whitelist(methods=["GET"])
def ping():
	"""Lets Solvronix Pilot see that the connector is installed (read-only, any desk user)."""
	return {
		"app": "solvronix_pilot_connector",
		"version": __version__,
		# get_cached_doc applies field defaults (same source as boot.py), get_single_value does not.
		"enabled": bool(frappe.get_cached_doc("Pilot Connector Settings").enabled),
	}
