# Copyright (c) 2026, Solvronix and contributors
import frappe

DOCTYPE = "Pilot Connector Settings"


def after_install():
	ensure_settings()


def ensure_settings():
	"""Store the settings defaults once, so every reader (boot, ping, reports) sees the same values.

	A Single is never saved on install. frappe.db.get_single_value then returns 0 for
	"enabled" even though the field defaults to 1.
	"""
	if frappe.db.exists("Singles", {"doctype": DOCTYPE}):
		return
	frappe.get_single(DOCTYPE).save(ignore_permissions=True)
