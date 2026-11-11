// Solvronix Pilot Connector: loads the Pilot chat button in the desk.
// The button code (pilot_widget.js) ships inside this app, so no script from another server
// ever runs in your ERPNext. Only the chat panel itself is loaded from Pilot, in an iframe,
// which cannot read or change the ERPNext page around it.
(function () {
	function load() {
		var cfg = frappe.boot && frappe.boot.pilot_connector;
		if (!cfg || document.getElementById("solvronix-pilot-widget-loader")) return;
		var s = document.createElement("script");
		s.id = "solvronix-pilot-widget-loader";
		s.async = true;
		s.src = "/assets/solvronix_pilot_connector/js/pilot_widget.js?v=" + encodeURIComponent(cfg.version || "1");
		s.setAttribute("data-pilot-url", cfg.pilot_url);
		s.setAttribute("data-site", cfg.site);
		s.setAttribute("data-position", cfg.position);
		if (frappe.boot.lang) s.setAttribute("data-lang", frappe.boot.lang);
		document.body.appendChild(s);
	}
	if (window.frappe && frappe.boot) load();
	else document.addEventListener("DOMContentLoaded", load);
})();
