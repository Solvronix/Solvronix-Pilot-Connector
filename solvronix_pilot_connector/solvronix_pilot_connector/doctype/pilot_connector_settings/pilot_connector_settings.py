# Copyright (c) 2026, Solvronix and contributors
from urllib.parse import urlparse

import frappe
from frappe import _
from frappe.model.document import Document

CHANGED_EVENT = "solvronix_pilot_connector_changed"


class PilotConnectorSettings(Document):
	def validate(self):
		url = urlparse((self.pilot_url or "").strip())
		if url.scheme != "https" or not url.hostname:
			frappe.throw(_("Pilot Address must start with https://"))
		self.pilot_url = f"https://{url.netloc}"

	def on_update(self):
		# Boot info carries the button settings: make every user pick up the change.
		frappe.clear_cache()
		# Open desks re-read their own button settings now (api.button_config), so a change
		# shows without a reload. The message carries nothing: each user's settings, roles
		# included, are checked on the server.
		frappe.publish_realtime(CHANGED_EVENT, {}, after_commit=True)
