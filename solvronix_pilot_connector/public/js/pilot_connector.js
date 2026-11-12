// Solvronix Pilot Connector: loads the Pilot chat button in the desk.
// The button code (pilot_widget.js) ships inside this app, so no script from another server
// ever runs in your ERPNext. Only the chat panel itself is loaded from Pilot, in an iframe,
// which cannot read or change the ERPNext page around it.
(function () {
	var LOADER = "solvronix-pilot-widget-loader";
	var CHANGED = "solvronix_pilot_connector_changed";

	function load() {
		var cfg = frappe.boot && frappe.boot.pilot_connector;
		if (!cfg || document.getElementById(LOADER)) return;
		var s = document.createElement("script");
		s.id = LOADER;
		s.async = true;
		s.src = "/assets/solvronix_pilot_connector/js/pilot_widget.js?v=" + encodeURIComponent(cfg.version || "1");
		s.setAttribute("data-pilot-url", cfg.pilot_url);
		s.setAttribute("data-site", cfg.site);
		s.setAttribute("data-position", cfg.position);
		if (frappe.boot.lang) s.setAttribute("data-lang", frappe.boot.lang);
		document.body.appendChild(s);
	}

	function unload() {
		["solvronix-pilot-widget", LOADER].forEach(function (id) {
			var el = document.getElementById(id);
			if (el) el.remove();
		});
		window.__solvronixPilotWidget = false;
	}

	// Settings were saved (here or in another tab or by another admin): ask the server for
	// this user's button again and rebuild it only if something changed. No reload needed.
	function refresh() {
		frappe.call({
			method: "solvronix_pilot_connector.api.button_config",
			type: "GET",
			callback: function (r) {
				var cfg = r.message || null;
				var now = (frappe.boot && frappe.boot.pilot_connector) || null;
				if (JSON.stringify(cfg) === JSON.stringify(now) && (!cfg || document.getElementById(LOADER))) return;
				frappe.boot.pilot_connector = cfg;
				unload();
				load();
			},
		});
	}

	function start() {
		load();
		if (frappe.realtime && frappe.realtime.on) frappe.realtime.on(CHANGED, refresh);
	}

	window.solvronixPilotConnector = { refresh: refresh };
	if (window.frappe && frappe.boot) start();
	else document.addEventListener("DOMContentLoaded", start);
})();
