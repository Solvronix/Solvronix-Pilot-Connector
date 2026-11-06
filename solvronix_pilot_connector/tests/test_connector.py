# Copyright (c) 2026, Solvronix and contributors
# Run on a site with the app installed:
#   bench --site <site> run-tests --app solvronix_pilot_connector

import frappe
from frappe.tests import IntegrationTestCase

from solvronix_pilot_connector import __version__
from solvronix_pilot_connector.api import ping
from solvronix_pilot_connector.boot import _boot


class TestConnector(IntegrationTestCase):
	def setUp(self):
		self.settings = frappe.get_single("Pilot Connector Settings")
		self.saved = self.settings.as_dict()

	def tearDown(self):
		frappe.set_user("Administrator")
		doc = frappe.get_single("Pilot Connector Settings")
		doc.update({k: self.saved.get(k) for k in ("enabled", "position", "pilot_url")})
		doc.set("allowed_roles", [{"role": r.role} for r in self.saved.get("allowed_roles") or []])
		doc.save()

	def test_ping_shape(self):
		self.assertEqual(ping(), {"app": "solvronix_pilot_connector", "version": __version__, "enabled": bool(self.settings.enabled)})

	def test_pilot_url_must_be_https(self):
		self.settings.pilot_url = "http://pilot.solvronix.com"
		self.assertRaises(frappe.ValidationError, self.settings.save)
		self.settings.pilot_url = "https://pilot.solvronix.com/some/path"
		self.settings.save()
		self.assertEqual(self.settings.pilot_url, "https://pilot.solvronix.com")

	def test_boot_respects_enabled_and_roles(self):
		self.settings.update({"enabled": 1, "pilot_url": "https://pilot.solvronix.com", "position": "Right"})
		self.settings.set("allowed_roles", [])
		self.settings.save()
		boot = frappe._dict()
		_boot(boot)
		self.assertEqual(boot.pilot_connector["position"], "right")

		self.settings.enabled = 0
		self.settings.save()
		boot = frappe._dict()
		_boot(boot)
		self.assertNotIn("pilot_connector", boot)
