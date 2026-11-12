// Copyright (c) 2026, Solvronix and contributors
// Apply the new button settings in this tab right after saving (no reload).
frappe.ui.form.on("Pilot Connector Settings", {
	after_save() {
		if (window.solvronixPilotConnector) window.solvronixPilotConnector.refresh();
	},
});
