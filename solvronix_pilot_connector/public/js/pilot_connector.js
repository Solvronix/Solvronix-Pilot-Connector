// Solvronix Pilot Connector: loads the Pilot chat button in the desk.
// The button and panel come from the Pilot server, so updates need nothing here.
(function () {
	function load() {
		var cfg = frappe.boot && frappe.boot.pilot_connector;
		if (!cfg || document.getElementById("solvronix-pilot-widget-loader")) return;
		var s = document.createElement("script");
		s.id = "solvronix-pilot-widget-loader";
		s.async = true;
		// Hourly stamp: widget updates on the Pilot server reach every site within an hour,
		// with no connector release (assets are otherwise cached for a year).
		s.src = cfg.pilot_url + "/assets/solvronix_pilot/js/pilot_widget.js?v=" + Math.floor(Date.now() / 3600000);
		s.setAttribute("data-site", cfg.site);
		s.setAttribute("data-position", cfg.position);
		if (frappe.boot.lang) s.setAttribute("data-lang", frappe.boot.lang);
		document.body.appendChild(s);
	}
	if (window.frappe && frappe.boot) load();
	else document.addEventListener("DOMContentLoaded", load);
})();
