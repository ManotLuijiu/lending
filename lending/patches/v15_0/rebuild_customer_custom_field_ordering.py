# -*- coding: utf-8 -*-
# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

"""
Migration patch to rebuild Customer DocType custom field ordering
Fixes idx=0 issue for all Lending custom fields which prevents proper field positioning
"""

import frappe


def execute():
	"""Rebuild Customer DocType to recalculate custom field idx values"""
	try:
		frappe.logger().info("Running patch: rebuild_customer_custom_field_ordering")

		# Clear cache first
		frappe.clear_cache(doctype="Customer")

		# Get Customer DocType
		customer_doctype = frappe.get_doc("DocType", "Customer")

		# Force save to trigger idx recalculation
		# This processes all insert_after relationships and assigns proper idx values
		customer_doctype.flags.ignore_validate = True
		customer_doctype.flags.ignore_mandatory = True
		customer_doctype.flags.ignore_permissions = True
		customer_doctype.save()

		# Clear cache again
		frappe.clear_cache(doctype="Customer")

		frappe.db.commit()

		frappe.logger().info("✅ Customer custom field ordering rebuilt successfully")

		# Log verification info
		sample_fields = [
			"ld_custom_debts_overview_section",
			"ld_custom_debts_overview",
			"ld_custom_contact_info",
		]

		frappe.logger().info("Verifying idx values:")
		for fieldname in sample_fields:
			field = frappe.db.get_value(
				"Custom Field",
				{"dt": "Customer", "fieldname": fieldname},
				["idx"],
				as_dict=True,
			)
			if field:
				frappe.logger().info(f"  {fieldname}: idx={field.idx}")

	except Exception as e:
		frappe.logger().error(f"Error in patch rebuild_customer_custom_field_ordering: {e}")
		import traceback

		frappe.logger().error(traceback.format_exc())
		# Don't raise - allow migration to continue
