# Copyright (c) 2026, Solvronix and contributors
"""Phone alerts: tell Solvronix Pilot about each new ERPNext notification (the bell).

Only the notification's name and its recipient are sent. Pilot then reads the
notification back from this ERPNext with that person's own Pilot login, so nothing can be
faked and Pilot never sees alerts of people who don't use Pilot alerts. Nothing is sent
while Pilot says alerts are off for this site (asked at most every 10 minutes).
"""

import frappe
import requests
from frappe.utils import get_host_name

from solvronix_pilot_connector import __version__

STATUS_KEY = "solvronix_pilot_connector:alerts_on"
STATUS_TTL = 600
TIMEOUT = 5


def on_notification(doc, method=None):
	"""Notification Log after_insert. Never raises: an ERPNext save must not fail because of Pilot."""
	try:
		if not doc.for_user or _settings() is None or frappe.cache.get_value(STATUS_KEY) == "0":
			return
		frappe.enqueue(
			"solvronix_pilot_connector.alerts.send",
			queue="short",
			enqueue_after_commit=True,
			name=doc.name,
			for_user=doc.for_user,
			site=get_host_name(),
		)
	except Exception:
		pass


def send(name: str, for_user: str, site: str):
	"""Background job: report one notification to Pilot (name and recipient only)."""
	settings = _settings()
	if settings is None or not pilot_wants_alerts(site):
		return
	try:
		requests.post(
			f"{_base(settings)}/api/method/solvronix_pilot.push.connector_event",
			data={"site": site, "name": name, "for_user": for_user, "version": __version__},
			timeout=TIMEOUT,
		)
	except requests.RequestException:
		pass  # Pilot unreachable: this alert is skipped, the next one tries again.


def pilot_wants_alerts(site: str) -> bool:
	cached = frappe.cache.get_value(STATUS_KEY)
	if cached is not None:
		return cached == "1"
	on = False
	settings = _settings()
	if settings is not None:
		try:
			resp = requests.get(
				f"{_base(settings)}/api/method/solvronix_pilot.push.connector_status",
				params={"site": site},
				timeout=TIMEOUT,
			)
			on = bool(resp.ok and (resp.json().get("message") or {}).get("on"))
		except (requests.RequestException, ValueError):
			on = False
	frappe.cache.set_value(STATUS_KEY, "1" if on else "0", expires_in_sec=STATUS_TTL)
	return on


def _settings():
	settings = frappe.get_cached_doc("Pilot Connector Settings")
	return settings if settings.enabled else None


def _base(settings) -> str:
	return (settings.pilot_url or "https://pilot.solvronix.com").rstrip("/")
