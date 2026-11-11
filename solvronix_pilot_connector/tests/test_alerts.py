# Copyright (c) 2026, Solvronix and contributors
# Run on a site with the app installed:
#   bench --site <site> run-tests --app solvronix_pilot_connector

from unittest.mock import MagicMock, patch

import frappe
from frappe.tests import IntegrationTestCase

from solvronix_pilot_connector import alerts


class TestAlerts(IntegrationTestCase):
	def setUp(self):
		frappe.cache.delete_value(alerts.STATUS_KEY)
		self.settings = frappe.get_single("Pilot Connector Settings")
		self.was_enabled = self.settings.enabled
		frappe.db.set_single_value("Pilot Connector Settings", "enabled", 1)
		frappe.clear_document_cache("Pilot Connector Settings", "Pilot Connector Settings")

	def tearDown(self):
		frappe.cache.delete_value(alerts.STATUS_KEY)
		frappe.db.set_single_value("Pilot Connector Settings", "enabled", self.was_enabled)
		frappe.clear_document_cache("Pilot Connector Settings", "Pilot Connector Settings")

	def _doc(self):
		return frappe._dict(name="NL-1", for_user="someone@example.com")

	def test_hook_queues_a_job_and_never_raises(self):
		with patch.object(frappe, "enqueue") as enqueue:
			alerts.on_notification(self._doc())
		enqueue.assert_called_once()
		self.assertEqual(enqueue.call_args.kwargs["name"], "NL-1")
		with patch.object(frappe, "enqueue", side_effect=Exception("redis down")):
			alerts.on_notification(self._doc())  # must not break the ERPNext save

	def test_hook_skips_when_pilot_said_off_or_connector_disabled(self):
		frappe.cache.set_value(alerts.STATUS_KEY, "0")
		with patch.object(frappe, "enqueue") as enqueue:
			alerts.on_notification(self._doc())
		enqueue.assert_not_called()
		frappe.cache.delete_value(alerts.STATUS_KEY)
		frappe.db.set_single_value("Pilot Connector Settings", "enabled", 0)
		frappe.clear_document_cache("Pilot Connector Settings", "Pilot Connector Settings")
		with patch.object(frappe, "enqueue") as enqueue:
			alerts.on_notification(self._doc())
		enqueue.assert_not_called()

	def test_send_asks_pilot_once_then_reports_name_and_user_only(self):
		status = MagicMock(ok=True)
		status.json.return_value = {"message": {"on": True}}
		with patch.object(alerts.requests, "get", return_value=status) as get, patch.object(alerts.requests, "post") as post:
			alerts.send("NL-1", "someone@example.com", "erp.example.com")
			alerts.send("NL-2", "someone@example.com", "erp.example.com")
		get.assert_called_once()  # cached for 10 minutes
		self.assertEqual(post.call_count, 2)
		self.assertEqual(set(post.call_args.kwargs["data"]), {"site", "name", "for_user", "version"})

	def test_send_does_nothing_while_pilot_says_off(self):
		status = MagicMock(ok=True)
		status.json.return_value = {"message": {"on": False}}
		with patch.object(alerts.requests, "get", return_value=status), patch.object(alerts.requests, "post") as post:
			alerts.send("NL-1", "someone@example.com", "erp.example.com")
		post.assert_not_called()

	def test_pilot_shortcut_redirects_to_this_site(self):
		from solvronix_pilot_connector.www import pilot as page

		frappe.db.set_single_value("Pilot Connector Settings", "enabled", 1)
		frappe.clear_document_cache("Pilot Connector Settings", "Pilot Connector Settings")
		with patch.object(page, "get_host_name", return_value="erp.example.com"):
			with self.assertRaises(frappe.Redirect) as r:
				page.get_context(frappe._dict())
		self.assertEqual(r.exception.http_status_code, 302)
		self.assertTrue(frappe.flags.redirect_location.endswith("/pilot?site=erp.example.com"))
