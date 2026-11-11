/* Solvronix Pilot chat widget.
 *
 *   <script src="https://pilot.solvronix.com/assets/solvronix_pilot/js/pilot_widget.js?v=1"
 *           data-site="erp.yourcompany.com" async></script>
 *
 * Adds a floating button (bottom right, or data-position="left") that opens Pilot in a
 * panel. Everything lives in a shadow root, so the host page's CSS can't touch it and
 * ours can't leak out. The panel iframe is created on first open only, so the host page
 * loads no Pilot code until someone asks for it.
 */
(function () {
	"use strict";
	if (window.__solvronixPilotWidget) return;
	window.__solvronixPilotWidget = true;

	var script = document.currentScript;
	// The connector app ships this file itself (no remote script in the client's ERPNext) and
	// names the Pilot server in data-pilot-url; a plain <script> embed uses the script's origin.
	var ORIGIN = (function () {
		var given = script && script.getAttribute("data-pilot-url");
		try {
			if (given && new URL(given).protocol === "https:") return new URL(given).origin;
			if (script && script.src) return new URL(script.src).origin;
		} catch (e) {}
		return "https://pilot.solvronix.com";
	})();
	var site = (script && script.getAttribute("data-site")) || "";
	var lang = (script && script.getAttribute("data-lang")) || "";
	var side = script && script.getAttribute("data-position") === "left" ? "left" : "right";
	var label = ((script && script.getAttribute("data-label")) || "Ask Pilot").replace(/[&<>"']/g, function (c) {
		return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
	});
	var STORE = "solvronix-pilot-open";

	var CHAT = '<img src="' + ORIGIN + '/assets/solvronix_pilot/images/pilot-s.png?v=3" width="38" height="38" alt="" draggable="false">';
	var CLOSE =
		'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>';

	var css =
		":host{all:initial}" +
		"*{box-sizing:border-box}" +
		".launcher{position:fixed;bottom:24px;" + side + ":24px;z-index:2147483000;width:62px;height:62px;border:1px solid #eeeef0;border-radius:50%;cursor:pointer;color:#0b1220;" +
		"background:#fff;box-shadow:0 10px 25px rgba(59,130,246,.28),0 2px 6px rgba(0,0,0,.1);" +
		"display:grid;place-items:center;transition:transform .18s ease,box-shadow .18s ease}" +
		".launcher:hover{transform:translateY(-2px) scale(1.04);box-shadow:0 14px 30px rgba(59,130,246,.38),0 2px 6px rgba(0,0,0,.1)}" +
		".launcher img{display:block;width:38px;height:38px;pointer-events:none}" +
		".launcher:focus-visible{outline:3px solid rgba(59,130,246,.45);outline-offset:3px}" +
		".launcher .ic{display:grid;place-items:center;transition:transform .2s ease,opacity .2s ease}" +
		".launcher .ic.close{position:absolute;opacity:0;transform:rotate(-90deg)}" +
		".open .launcher .ic.chat{opacity:0;transform:rotate(90deg)}" +
		".open .launcher .ic.close{opacity:1;transform:none}" +
		".tip{position:fixed;bottom:36px;" + side + ":96px;z-index:2147483000;padding:8px 14px;border-radius:999px;background:#fff;color:#0a0a0b;" +
		"font:500 13px/1.2 Inter,system-ui,-apple-system,'Segoe UI',sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.12);border:1px solid #eeeef0;" +
		"opacity:0;transform:translateY(6px);pointer-events:none;transition:opacity .2s,transform .2s;white-space:nowrap}" +
		".tip::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:#22d3ee;box-shadow:0 0 8px #22d3ee;margin-" + (side === "right" ? "right" : "left") + ":8px;vertical-align:1px}" +
		".launcher:hover+.tip,.tip.show{opacity:1;transform:none}" +
		".open .tip{display:none}" +
		".panel{position:fixed;bottom:96px;" + side + ":24px;z-index:2147483001;width:400px;height:min(660px,calc(100vh - 120px));border-radius:20px;overflow:hidden;" +
		"background:#fff;border:1px solid #eeeef0;box-shadow:0 24px 60px rgba(0,0,0,.18),0 4px 12px rgba(0,0,0,.06);" +
		"transform-origin:bottom " + side + ";opacity:0;transform:translateY(12px) scale(.96);pointer-events:none;visibility:hidden;" +
		"transition:opacity .18s ease,transform .18s ease,visibility 0s linear .18s}" +
		".open .panel{opacity:1;transform:none;pointer-events:auto;visibility:visible;transition:opacity .18s ease,transform .18s ease}" +
		".panel iframe{width:100%;height:100%;border:0;display:block;background:#fff}" +
		".loading{position:absolute;inset:0;display:grid;place-items:center;background:#fff}" +
		".loading i{width:28px;height:28px;border-radius:50%;border:3px solid #e4e4e7;border-top-color:#3b82f6;animation:spin .8s linear infinite}" +
		"@keyframes spin{to{transform:rotate(360deg)}}" +
		"@media (max-width:600px){.panel{inset:0;width:auto;height:auto;border-radius:0;border:0}.open .launcher{display:none}.tip{display:none}}" +
		"@media (prefers-reduced-motion:reduce){.launcher,.panel,.tip,.launcher .ic{transition:none}}";

	function build() {
		var host = document.createElement("div");
		host.id = "solvronix-pilot-widget";
		var root = host.attachShadow ? host.attachShadow({ mode: "open" }) : host;
		var wrap = document.createElement("div");
		wrap.innerHTML =
			"<style>" + css + "</style>" +
			'<button class="launcher" type="button" aria-label="' + label + '" aria-expanded="false">' +
			'<span class="ic chat">' + CHAT + '</span><span class="ic close">' + CLOSE + "</span></button>" +
			'<div class="tip" role="status">' + label + "</div>" +
			'<div class="panel" role="dialog" aria-label="Solvronix Pilot"></div>';
		root.appendChild(wrap);
		document.body.appendChild(host);

		var btn = wrap.querySelector(".launcher");
		var panel = wrap.querySelector(".panel");
		var tip = wrap.querySelector(".tip");
		var frame = null;

		function src() {
			var q = ["embed=1"];
			if (site) q.push("site=" + encodeURIComponent(site));
			if (lang) q.push("_lang=" + encodeURIComponent(lang));
			return ORIGIN + "/pilot?" + q.join("&");
		}

		function ensureFrame() {
			if (frame) return;
			panel.innerHTML = '<div class="loading"><i></i></div>';
			frame = document.createElement("iframe");
			frame.title = "Solvronix Pilot";
			frame.allow = "clipboard-write";
			frame.src = src();
			frame.onload = function () {
				var l = panel.querySelector(".loading");
				if (l) l.remove();
			};
			panel.appendChild(frame);
		}

		function open() {
			ensureFrame();
			wrap.classList.add("open");
			btn.setAttribute("aria-expanded", "true");
			btn.setAttribute("aria-label", "Close");
			try { sessionStorage.setItem(STORE, "1"); } catch (e) {}
			setTimeout(function () {
				try {
					frame.focus();
					frame.contentWindow.postMessage({ type: "solvronix-pilot:opened" }, ORIGIN);
				} catch (e) {}
			}, 200);
		}

		function close() {
			wrap.classList.remove("open");
			btn.setAttribute("aria-expanded", "false");
			btn.setAttribute("aria-label", label);
			try { sessionStorage.removeItem(STORE); } catch (e) {}
		}

		btn.addEventListener("click", function () {
			wrap.classList.contains("open") ? close() : open();
		});
		document.addEventListener("keydown", function (e) {
			if (e.key === "Escape" && wrap.classList.contains("open")) close();
		});
		window.addEventListener("message", function (e) {
			if (e.origin === ORIGIN && e.data && e.data.type === "solvronix-pilot:close") {
				close();
				btn.focus();
			}
		});

		// Warm the connection while the user is still reading the page.
		var hint = document.createElement("link");
		hint.rel = "preconnect";
		hint.href = ORIGIN;
		document.head.appendChild(hint);
		// Load the panel quietly once the host page is idle, so the first click is instant.
		// It stays hidden (and never takes focus) until opened; hovering the button starts it sooner.
		btn.addEventListener("pointerenter", ensureFrame, { once: true });
		btn.addEventListener("focus", ensureFrame, { once: true });
		var idle = window.requestIdleCallback || function (fn) { return setTimeout(fn, 1); };
		setTimeout(function () { idle(ensureFrame, { timeout: 3000 }); }, 2500);

		// Stay open across page loads in the same tab, like other chat widgets.
		var reopen = false;
		try { reopen = sessionStorage.getItem(STORE) === "1"; } catch (e) {}
		if (reopen) open();
		else {
			setTimeout(function () { tip.classList.add("show"); }, 1500);
			setTimeout(function () { tip.classList.remove("show"); }, 6500);
		}
	}

	if (document.body) build();
	else document.addEventListener("DOMContentLoaded", build);
})();
