# Copyright (c) 2026, Solvronix and contributors
import frappe

from solvronix_pilot_connector import __version__


@frappe.whitelist(methods=["GET"])
def ping():
	"""Lets Solvronix Pilot see that the connector is installed (read-only, any desk user)."""
	return {
		"app": "solvronix_pilot_connector",
		"version": __version__,
		"enabled": bool(frappe.db.get_single_value("Pilot Connector Settings", "enabled")),
	}
