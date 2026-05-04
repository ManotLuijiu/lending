# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Company": [
				{
					"fieldname": "nano_finance_section",
					"fieldtype": "Section Break",
					"label": "Nano Finance",
					"insert_after": "purchase_expense_contra_account",
				},
				{
					"fieldname": "accrual_loan_debtor",
					"fieldtype": "Link",
					"label": "Accrual Loan Debtor",
					"options": "Account",
					"insert_after": "nano_finance_section",
				},
				{
					"fieldname": "accrual_loan_creditor",
					"fieldtype": "Link",
					"label": "Accrual Loan Creditor",
					"options": "Account",
					"insert_after": "accrual_loan_debtor",
				},
			]
		},
		ignore_validate=True,
	)
