app_name = "solvronix_pilot_connector"
app_title = "Solvronix Pilot Connector"
app_publisher = "Solvronix"
app_description = "Adds the Solvronix Pilot assistant button to ERPNext"
app_email = "sales@solvronix.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "solvronix_pilot_connector",
# 		"logo": "/assets/solvronix_pilot_connector/logo.png",
# 		"title": "Solvronix Pilot Connector",
# 		"route": "/solvronix_pilot_connector",
# 		"has_permission": "solvronix_pilot_connector.api.permission.has_app_permission",
# 	}
# ]

# The dock, the rail down the left of the desk, is a document rather than a hook. Author it in
# Manage Dock on a developer-mode site and press Export to App, and it is written to
# `solvronix_pilot_connector/dock/solvronix_pilot_connector/solvronix_pilot_connector.json` for git to carry. An app that ships none has no
# rail: its sidebar gets a switcher in the header instead.
#
# A companion app, one that extends a host app rather than standing on its own, says so with
# `mount_on` on that same record, and its entries are appended to the host's rail. Mounting keeps
# the companion off the apps screen, so it takes precedence over any add_to_apps_screen above.

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/solvronix_pilot_connector/css/solvronix_pilot_connector.css"
app_include_js = "/assets/solvronix_pilot_connector/js/pilot_connector.js?v=5"

# include js, css files in header of web template
# web_include_css = "/assets/solvronix_pilot_connector/css/solvronix_pilot_connector.css"
# web_include_js = "/assets/solvronix_pilot_connector/js/solvronix_pilot_connector.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "solvronix_pilot_connector/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_kanban_js = {"doctype" : "public/js/doctype_kanban.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "solvronix_pilot_connector/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "solvronix_pilot_connector.utils.jinja_methods",
# 	"filters": "solvronix_pilot_connector.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "solvronix_pilot_connector.install.before_install"
after_install = "solvronix_pilot_connector.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "solvronix_pilot_connector.uninstall.before_uninstall"
# after_uninstall = "solvronix_pilot_connector.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "solvronix_pilot_connector.utils.before_app_install"
# after_app_install = "solvronix_pilot_connector.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "solvronix_pilot_connector.utils.before_app_uninstall"
# after_app_uninstall = "solvronix_pilot_connector.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "solvronix_pilot_connector.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "solvronix_pilot_connector.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["solvronix_pilot_connector.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"solvronix_pilot_connector.tasks.all"
# 	],
# 	"daily": [
# 		"solvronix_pilot_connector.tasks.daily"
# 	],
# 	"hourly": [
# 		"solvronix_pilot_connector.tasks.hourly"
# 	],
# 	"weekly": [
# 		"solvronix_pilot_connector.tasks.weekly"
# 	],
# 	"monthly": [
# 		"solvronix_pilot_connector.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "solvronix_pilot_connector.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "solvronix_pilot_connector.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "solvronix_pilot_connector.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "solvronix_pilot_connector.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["solvronix_pilot_connector.utils.before_request"]
# after_request = ["solvronix_pilot_connector.utils.after_request"]

# Job Events
# ----------
# before_job = ["solvronix_pilot_connector.utils.before_job"]
# after_job = ["solvronix_pilot_connector.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"solvronix_pilot_connector.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []


boot_session = "solvronix_pilot_connector.boot.boot_session"

# Phone alerts: report each new ERPNext notification (the bell) to Pilot (alerts.py).
doc_events = {"Notification Log": {"after_insert": "solvronix_pilot_connector.alerts.on_notification"}}
