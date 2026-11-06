# Copyright (c) 2026, Solvronix and contributors
from urllib.parse import urlparse

import frappe
from frappe import _
from frappe.model.document import Document


class PilotConnectorSettings(Document):
	def validate(self):
		url = urlparse((self.pilot_url or "").strip())
		if url.scheme != "https" or not url.hostname:
			frappe.throw(_("Pilot Address must start with https://"))
		self.pilot_url = f"https://{url.netloc}"

	def on_update(self):
		# Boot info carries the button settings: make every user pick up the change.
		frappe.clear_cache()
